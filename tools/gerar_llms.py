#!/usr/bin/env python3
"""Gera llms.txt e llms-full.txt para que sistemas de IA leiam o site.

llms.txt      índice em markdown, com uma linha por página
llms-full.txt texto integral do site em um arquivo só

Por que existe: buscadores tradicionais rastreiam HTML; assistentes de IA
funcionam melhor com markdown limpo. Sem isso, a IA precisa interpretar
marcação Tailwind e costuma errar ou resumir mal.

O formato segue a proposta do llmstxt.org: H1 com o nome, blockquote de resumo,
e listas em H2 com `[Título](URL): descrição`.

    python3 tools/gerar_llms.py
"""
from __future__ import annotations

import html
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORA = {'404.html', 'pendencias.html', 'styleguide.html'}

GRUPOS = [
    ('Institucional', ['index.html', 'quem-somos.html', 'impacto.html', 'transparencia.html']),
    ('Projetos', ['projetos.html']),
    ('Participação', ['doe.html', 'como-ajudar.html', 'contato.html', 'noticias.html']),
    ('Políticas', ['politica-privacidade.html']),
]


def texto_da_pagina(caminho: str) -> str:
    """Extrai o texto visível, preservando a hierarquia de títulos e listas."""
    with open(caminho, encoding='utf-8') as fh:
        doc = fh.read()

    corpo = doc[doc.find('<main'):doc.find('<footer')]
    corpo = re.sub(r'<script.*?</script>', '', corpo, flags=re.S)
    corpo = re.sub(r'<nav\b.*?</nav>', '', corpo, flags=re.S)
    # figcaption vira legenda de imagem; o alt já descreve a foto
    corpo = re.sub(r'<figcaption[^>]*>(.*?)</figcaption>', r'\n[foto] \1\n', corpo, flags=re.S)
    corpo = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*>', r'\n[imagem] \1\n', corpo)

    for n in range(1, 5):
        corpo = re.sub(rf'<h{n}[^>]*>(.*?)</h{n}>', lambda m, n=n: f'\n\n{"#"*n} {m.group(1)}\n', corpo, flags=re.S)
    corpo = re.sub(r'<li[^>]*>(.*?)</li>', r'\n- \1', corpo, flags=re.S)
    corpo = re.sub(r'<(p|dd|dt|summary|blockquote)[^>]*>(.*?)</\1>', r'\n\2\n', corpo, flags=re.S)
    corpo = re.sub(r'<th[^>]*>(.*?)</th>', r' | \1', corpo, flags=re.S)
    corpo = re.sub(r'<td[^>]*>(.*?)</td>', r' | \1', corpo, flags=re.S)
    corpo = re.sub(r'</tr>', '\n', corpo)

    corpo = re.sub(r'<[^>]+>', ' ', corpo)
    corpo = html.unescape(corpo)
    corpo = re.sub(r'[ \t]+', ' ', corpo)
    corpo = re.sub(r' *\n *', '\n', corpo)
    corpo = re.sub(r'\n{3,}', '\n\n', corpo)
    return corpo.strip()


def main() -> int:
    with open(os.path.join(RAIZ, 'tools', 'site.json'), encoding='utf-8') as fh:
        cfg = json.load(fh)
    base = cfg['base_url'].rstrip('/')
    paginas = cfg['paginas']

    resumo = (
        '> ONG fundada em 13 de setembro de 1988 por mães trabalhadoras do bairro São Benedito, '
        'em Vitória, Espírito Santo, Brasil. Atende gratuitamente crianças e adolescentes de 6 a 17 anos '
        'no Território do Bem, região formada por 6 bairros e 3 comunidades no alto da cidade. '
        'Mantém 8 projetos de música, esporte, dança, reforço escolar e convivência, além de um '
        'programa para pessoas com mais de 50 anos. CNPJ 31.795.321/0001-53.'
    )

    linhas = ['# SECRI - Serviço de Engajamento Comunitário', '', resumo, '',
              'Em 2025 o SECRI serviu 7.041 refeições, atendeu 94 crianças e adolescentes, '
              'acompanhou 68 famílias e manteve 28 parcerias institucionais.', '']

    projetos = sorted(
        (p for p in paginas if p.startswith('projetos/')),
        key=lambda p: paginas[p]['title'])

    for titulo, chaves in GRUPOS:
        itens = []
        for pag in chaves:
            if pag not in paginas or pag in FORA:
                continue
            meta = paginas[pag]
            url = base + '/' + ('' if pag == 'index.html' else pag)
            nome = meta.get('breadcrumb') or meta['title'].split('|')[0].strip()
            itens.append(f'- [{nome}]({url}): {meta["description"]}')
        if titulo == 'Projetos':
            for pag in projetos:
                meta = paginas[pag]
                nome = meta['title'].split('|')[0].strip()
                itens.append(f'- [{nome}]({base}/{pag}): {meta["description"]}')
        if itens:
            linhas.append(f'## {titulo}')
            linhas.append('')
            linhas += itens
            linhas.append('')

    linhas += ['## Contato', '',
               '- Endereço: Rua Tenente Setúbal, 395, São Benedito, Vitória/ES, CEP 29047-850',
               '- WhatsApp e telefone: (27) 99849-9507',
               '- Telefone fixo: (27) 3215-0942',
               '- E-mail: contato@secri.org.br',
               '- E-mail para parcerias e doações de empresas: financeiro@secri.org.br',
               '- Instagram: https://instagram.com/ong_secri',
               '- YouTube: https://www.youtube.com/@secri-servicodeengajamento8817',
               '- Mapa: https://maps.app.goo.gl/X6PTheesC7vhV7ss8',
               '- Pix (CNPJ): 31.795.321/0001-53',
               '- Conta bancária: SICOOB 756, agência 3010, conta corrente 56729-9',
               '',
               '## Observação sobre esta versão', '',
               'O site está em fase de validação com a instituição. Trechos marcados como '
               '"a confirmar" ainda não foram verificados e não devem ser citados como fato. '
               'Os depoimentos publicados são ilustrativos e não correspondem a pessoas reais.',
               '',
               '## Outros formatos', '',
               f'- [Conteúdo integral em markdown]({base}/llms-full.txt)',
               f'- [Sitemap XML]({base}/sitemap.xml)',
               '']

    with open(os.path.join(RAIZ, 'llms.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(linhas))

    # ---- conteúdo integral -------------------------------------------------
    ordem = [p for _, ch in GRUPOS for p in ch if p in paginas] + projetos
    partes = ['# SECRI - Serviço de Engajamento Comunitário', '', resumo, '',
              'Conteúdo integral do site em texto. Gerado automaticamente a partir das páginas '
              f'publicadas em {base}/.', '', '---', '']
    for pag in ordem:
        caminho = os.path.join(RAIZ, pag)
        if not os.path.exists(caminho) or pag in FORA:
            continue
        url = base + '/' + ('' if pag == 'index.html' else pag)
        partes += [f'<!-- fonte: {url} -->', '', texto_da_pagina(caminho), '', '---', '']

    conteudo = '\n'.join(partes)
    with open(os.path.join(RAIZ, 'llms-full.txt'), 'w', encoding='utf-8') as fh:
        fh.write(conteudo)

    print(f'llms.txt: {len(linhas)} linhas')
    print(f'llms-full.txt: {len(ordem)} páginas · {len(conteudo)//1024} KB')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
