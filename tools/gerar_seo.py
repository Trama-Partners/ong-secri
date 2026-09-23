#!/usr/bin/env python3
"""Gera sitemap.xml e robots.txt a partir do site.json e dos arquivos em disco.

O sitemap inclui as imagens de cada página (extensão `image:` do protocolo).
Para uma ONG isso importa mais do que parece: boa parte do tráfego de descoberta
de projeto social chega pela busca por imagem.

    python3 tools/gerar_seo.py
"""
from __future__ import annotations

import datetime
import html
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# páginas que existem, mas não devem ser indexadas nem anunciadas
FORA = {'404.html', 'pendencias.html', 'styleguide.html'}

# quanto cada página pesa dentro do site, para o rastreador priorizar
PRIORIDADE = {
    'index.html': '1.0', 'projetos.html': '0.9', 'como-ajudar.html': '0.9',
    'quem-somos.html': '0.8', 'impacto.html': '0.8',
    'transparencia.html': '0.7', 'contato.html': '0.7',
    'noticias.html': '0.6', 'politica-privacidade.html': '0.3',
}


def modificado_em(caminho: str) -> str:
    """lastmod a partir da data real do arquivo, não de uma data fixa."""
    ts = os.path.getmtime(caminho)
    return datetime.date.fromtimestamp(ts).isoformat()


def imagens_da_pagina(caminho: str, base_url: str) -> list[tuple[str, str]]:
    """Devolve (url absoluta, texto alternativo) de cada foto de conteúdo.

    Logos de chrome ficam de fora: repetidos em toda página, só poluiriam
    o sitemap sem ajudar ninguém a encontrar nada.
    """
    with open(caminho, encoding='utf-8') as fh:
        txt = fh.read()
    achados = []
    for tag in re.findall(r'<img\b[^>]*>', txt):
        src = re.search(r'src="([^"]+)"', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        if not src:
            continue
        rel = src.group(1).lstrip('./').replace('../', '')
        if '/fotos/' not in rel and '/parceiros/' not in rel:
            continue
        achados.append((f'{base_url}/{rel}', alt.group(1) if alt else ''))
    # mantém a ordem de aparição e remove repetidas
    vistas, unicas = set(), []
    for url, alt in achados:
        if url not in vistas:
            vistas.add(url)
            unicas.append((url, alt))
    return unicas


def main() -> int:
    with open(os.path.join(RAIZ, 'tools', 'site.json'), encoding='utf-8') as fh:
        cfg = json.load(fh)
    base = cfg['base_url'].rstrip('/')

    entradas = []
    total_img = 0
    for pag in sorted(cfg['paginas']):
        if pag in FORA:
            continue
        caminho = os.path.join(RAIZ, pag)
        if not os.path.exists(caminho):
            print(f'  AUSENTE {pag}')
            continue

        loc = base + '/' + ('' if pag == 'index.html' else pag)
        imgs = imagens_da_pagina(caminho, base)
        total_img += len(imgs)

        blocos = ''.join(
            f'\n    <image:image>'
            f'\n      <image:loc>{html.escape(u)}</image:loc>'
            + (f'\n      <image:title>{html.escape(a)}</image:title>' if a else '')
            + '\n    </image:image>'
            for u, a in imgs)

        entradas.append(
            f'  <url>\n    <loc>{loc}</loc>'
            f'\n    <lastmod>{modificado_em(caminho)}</lastmod>'
            f'\n    <priority>{PRIORIDADE.get(pag, "0.8")}</priority>'
            f'{blocos}\n  </url>')

    with open(os.path.join(RAIZ, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
                 '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
                 + '\n'.join(entradas) + '\n</urlset>\n')

    with open(os.path.join(RAIZ, 'robots.txt'), 'w', encoding='utf-8') as fh:
        fh.write('User-agent: *\nAllow: /\n\n'
                 '# páginas internas de revisão, fora do índice\n'
                 + ''.join(f'Disallow: /{p}\n' for p in sorted(FORA))
                 + '\n# arquivos de trabalho, não são conteúdo do site\n'
                   'Disallow: /tools/\n\n'
                 f'Sitemap: {base}/sitemap.xml\n')

    print(f'sitemap.xml: {len(entradas)} URLs · {total_img} imagens')
    print('robots.txt atualizado')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
