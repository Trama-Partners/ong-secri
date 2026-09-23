#!/usr/bin/env python3
"""Sincroniza o header, o footer e o <head> de todas as páginas do site.

Por que isto existe
-------------------
O site é HTML estático puro, sem build, e precisa continuar assim: o cliente
abre o arquivo direto do disco. Includes por JavaScript não servem, porque
`fetch()` é bloqueado em `file://` e o site abriria sem header nem footer.

Então o chrome continua copiado em cada arquivo — mas escrito por este script
a partir de uma fonte única, em vez de na mão em 18 arquivos.

Como usar
---------
    python3 tools/sync_chrome.py --check     # só compara, não escreve
    python3 tools/sync_chrome.py --apply     # escreve

O corpo de cada página (entre `<main>` e `</main>`) nunca é tocado.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTIALS = os.path.join(RAIZ, 'tools', 'partials')

CLASSES = {
    'desktop_ativo': 'border-b-2 pb-1 text-sm font-semibold transition-colors border-rose-500 text-rose-700',
    'desktop_inativo': ('border-b-2 pb-1 text-sm font-semibold transition-colors border-transparent '
                        'text-ink-600 hover:border-rose-300 hover:text-ink-900'),
    'mobile_ativo': 'rounded-lg px-3 py-2.5 text-base font-semibold bg-rose-50 text-rose-700',
    'mobile_inativo': ('rounded-lg px-3 py-2.5 text-base font-semibold text-ink-600 '
                       'hover:bg-ink-50 hover:text-ink-900'),
}


ORGANIZACAO = {
    '@type': 'NGO',
    'name': 'SECRI',
    'alternateName': 'Serviço de Engajamento Comunitário',
    'url': 'https://secri.org.br/',
    'taxID': '31.795.321/0001-53',
}


def monta_jsonld(cfg: dict, rel: str, meta: dict) -> str:
    """Dados estruturados das páginas institucionais.

    As páginas de projeto trazem os seus no corpo, escritos por
    gerar_projetos.py a partir dos markdowns; aqui elas são puladas para não
    duplicar o mesmo tipo duas vezes no documento.
    """
    if meta.get('noindex') or rel.startswith('projetos/'):
        return ''

    base = cfg['base_url'].rstrip('/')
    url = base + '/' + ('' if rel == 'index.html' else rel)
    blocos = []

    tipo = meta.get('schema', 'WebPage')
    pagina = {
        '@context': 'https://schema.org',
        '@type': tipo,
        'name': meta['title'],
        'description': meta['description'],
        'url': url,
        'inLanguage': 'pt-BR',
        'isPartOf': {'@type': 'WebSite', 'name': 'SECRI', 'url': base + '/'},
        'publisher': ORGANIZACAO,
    }
    if meta.get('og_image'):
        pagina['primaryImageOfPage'] = {
            '@type': 'ImageObject',
            'url': f'{base}/{meta["og_image"]}',
            'width': meta.get('og_image_w'),
            'height': meta.get('og_image_h'),
            'caption': meta.get('og_image_alt', ''),
        }
    blocos.append(pagina)

    # trilha de navegação: ajuda o Google a exibir o caminho no resultado
    if rel != 'index.html':
        blocos.append({
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': base + '/'},
                {'@type': 'ListItem', 'position': 2,
                 'name': meta.get('breadcrumb', meta['title'].split('|')[0].strip()),
                 'item': url},
            ]})

    return '\n'.join(
        '<script type="application/ld+json">\n'
        + json.dumps(b, ensure_ascii=False, indent=2) + '\n</script>' for b in blocos)


def le(nome: str) -> str:
    with open(os.path.join(PARTIALS, nome), encoding='utf-8') as fh:
        return fh.read()


def monta_nav(cfg: dict, ativo: str | None, base: str, mobile: bool) -> str:
    linhas = []
    recuo = '      ' if mobile else '      '
    for item in cfg['nav']:
        é_ativo = item['chave'] == ativo
        tipo = ('mobile_' if mobile else 'desktop_') + ('ativo' if é_ativo else 'inativo')
        marca = ' aria-current="page"' if é_ativo else ''
        linhas.append(f'{recuo}<a href="{base}{item["href"]}"{marca} '
                      f'class="{CLASSES[tipo]}">{item["rotulo"]}</a>')
    return '\n'.join(linhas)


def monta_telefones(cfg: dict) -> str:
    return '\n'.join(
        f'        <li><a href="tel:{t["tel"]}" class="text-white hover:text-gold-500">{t["rotulo"]}</a></li>'
        for t in cfg['telefones']
    )


def chrome_da_pagina(cfg: dict, caminho_rel: str, meta: dict) -> tuple[str, str, str]:
    """Devolve (head, header, footer) já renderizados para uma página."""
    profundidade = caminho_rel.count('/')
    base = './' if profundidade == 0 else '../' * profundidade

    url = cfg['base_url'].rstrip('/') + '/' + ('' if caminho_rel == 'index.html' else caminho_rel)
    og = meta.get('og_image', 'assets/fotos/canoa-viva/canoa-02.webp')
    og_alt = meta.get('og_image_alt',
                      'Adolescentes do SECRI carregando juntos a canoa havaiana Benedito na praia')

    head = (le('head.html')
            .replace('{{TITLE}}', meta['title'])
            .replace('{{DESCRIPTION}}', meta['description'])
            .replace('{{ROBOTS}}',
                     '<meta name="robots" content="noindex, nofollow">\n'
                     if meta.get('noindex') else '')
            .replace('{{CANONICAL}}', url)
            .replace('{{OG_IMAGE}}', cfg['base_url'].rstrip('/') + '/' + og)
            .replace('{{OG_IMAGE_ALT}}', og_alt)
            .replace('{{OG_IMAGE_W}}', str(meta.get('og_image_w', '')))
            .replace('{{OG_IMAGE_H}}', str(meta.get('og_image_h', '')))
            .replace('{{JSONLD}}', monta_jsonld(cfg, caminho_rel, meta))
            .replace('{{BASE}}', base))

    header = (le('header.html')
              .replace('{{NAV_DESKTOP}}', monta_nav(cfg, meta.get('nav'), base, mobile=False))
              .replace('{{NAV_MOBILE}}', monta_nav(cfg, meta.get('nav'), base, mobile=True))
              .replace('{{BASE}}', base))

    footer = (le('footer.html')
              .replace('{{TELEFONES}}', monta_telefones(cfg))
              .replace('{{PAGINA_PROJETOS}}', cfg['pagina_projetos'])
              .replace('{{ROTULO_PROJETOS}}', cfg['rotulo_projetos'])
              .replace('{{BASE}}', base))

    return head, header, footer


def fatia(texto: str) -> tuple[str, str, str, str]:
    """Separa a página em (head, header, corpo, footer).

    Usa as fronteiras estruturais do documento em vez de números de linha:
    `<body ...>` fecha o head, `<main` abre o corpo e `<footer` abre o rodapé.
    """
    m_body = re.search(r'<body[^>]*>\n', texto)
    m_main = re.search(r'^<main', texto, re.M)
    m_footer = re.search(r'^<footer', texto, re.M)
    if not (m_body and m_main and m_footer):
        raise ValueError('estrutura inesperada: faltou <body>, <main> ou <footer>')
    return (texto[:m_body.end()],
            texto[m_body.end():m_main.start()],
            texto[m_main.start():m_footer.start()],
            texto[m_footer.start():])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='escreve as alterações')
    ap.add_argument('--check', action='store_true', help='só compara (padrão)')
    args = ap.parse_args()
    escrever = args.apply

    with open(os.path.join(RAIZ, 'tools', 'site.json'), encoding='utf-8') as fh:
        cfg = json.load(fh)

    divergentes = ausentes = iguais = 0
    for rel, meta in sorted(cfg['paginas'].items()):
        caminho = os.path.join(RAIZ, rel)
        if not os.path.exists(caminho):
            print(f'  AUSENTE     {rel}')
            ausentes += 1
            continue

        with open(caminho, encoding='utf-8') as fh:
            atual = fh.read()

        try:
            head_a, header_a, corpo, footer_a = fatia(atual)
        except ValueError as e:
            print(f'  ERRO        {rel}: {e}')
            divergentes += 1
            continue

        head_n, header_n, footer_n = chrome_da_pagina(cfg, rel, meta)
        novo = head_n + header_n + corpo + footer_n

        if novo == atual:
            iguais += 1
            continue

        divergentes += 1
        partes = [nome for nome, a, b in
                  (('head', head_a, head_n), ('header', header_a, header_n), ('footer', footer_a, footer_n))
                  if a != b]
        print(f'  {"atualizado" if escrever else "DIFERENTE ":11} {rel:34} ({", ".join(partes)})')
        if escrever:
            with open(caminho, 'w', encoding='utf-8') as fh:
                fh.write(novo)

    print(f'\n{iguais} iguais · {divergentes} {"atualizadas" if escrever else "divergentes"}'
          + (f' · {ausentes} ausentes' if ausentes else ''))
    if not escrever and divergentes:
        print('Nada foi escrito. Rode com --apply para aplicar.')
    return 1 if (ausentes or (divergentes and not escrever)) else 0


if __name__ == '__main__':
    sys.exit(main())
