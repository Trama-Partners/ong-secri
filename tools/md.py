#!/usr/bin/env python3
"""Conversor de Markdown para HTML, pequeno e sob medida.

Cobre só o que os arquivos de conteúdo do SECRI usam: parágrafos, títulos,
listas, negrito, itálico, código, links e tabelas. Nada de dependência externa.

A marcação `A CONFIRMAR` vira um selo visual em vez de texto solto — é a peça
que faz a versão de validação funcionar: o cliente enxerga o que falta.
"""
from __future__ import annotations

import html
import re

SELO_CONFIRMAR = (
    '<span class="inline-flex items-center gap-1 rounded-full bg-gold-100 px-2.5 py-0.5 '
    'text-xs font-bold uppercase tracking-wide text-gold-700 ring-1 ring-gold-300" '
    'title="Informação ainda não confirmada pelo SECRI">a confirmar</span>'
)


def inline(txt: str) -> str:
    """Formatação dentro de uma linha. Escapa o HTML antes de qualquer coisa."""
    txt = html.escape(txt, quote=False)
    txt = re.sub(r'`([^`]+)`', r'<code class="rounded bg-ink-100 px-1.5 py-0.5 text-[0.9em]">\1</code>', txt)
    txt = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                 r'<a href="\2" class="font-semibold text-sky-700 underline underline-offset-2 '
                 r'hover:text-rose-700">\1</a>', txt)
    txt = re.sub(r'\*\*([^*]+)\*\*', r'<strong class="font-semibold text-ink-900">\1</strong>', txt)
    txt = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<em>\1</em>', txt)
    # o marcador precisa vir depois do escape, senão o HTML do selo seria escapado
    txt = txt.replace('A CONFIRMAR', SELO_CONFIRMAR)
    return txt


def _tabela(linhas: list[str]) -> str:
    celulas = [[c.strip() for c in l.strip().strip('|').split('|')] for l in linhas]
    cab, corpo = celulas[0], celulas[2:]
    th = ''.join(f'<th scope="col" class="px-4 py-3 text-left font-display text-xs font-bold '
                 f'uppercase tracking-wide text-ink-600">{inline(c)}</th>' for c in cab)
    trs = []
    for linha in corpo:
        tds = ''.join(f'<td class="px-4 py-3 align-top text-ink-800">{inline(c)}</td>' for c in linha)
        trs.append(f'<tr class="border-t border-ink-200">{tds}</tr>')
    return ('<div class="overflow-x-auto"><table class="w-full border-collapse text-sm">'
            f'<thead class="bg-ink-50"><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>')


def render(md: str, nivel_titulo: int = 2) -> str:
    """Converte um trecho de Markdown. `nivel_titulo` define o que `##` vira."""
    saida: list[str] = []
    linhas = md.split('\n')
    i = 0
    while i < len(linhas):
        linha = linhas[i]
        cru = linha.strip()

        if not cru:
            i += 1
            continue

        # observações internas do time não vão para o site
        if cru.startswith('>'):
            i += 1
            continue

        if cru.startswith('|') and i + 1 < len(linhas) and set(linhas[i+1].strip()) <= set('|-: '):
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith('|'):
                bloco.append(linhas[i])
                i += 1
            saida.append(_tabela(bloco))
            continue

        m = re.match(r'^(#{1,6})\s+(.*)$', cru)
        if m:
            n = min(len(m.group(1)) + nivel_titulo - 2, 6)
            tam = {2: 'text-2xl sm:text-3xl', 3: 'text-xl sm:text-2xl'}.get(n, 'text-lg sm:text-xl')
            saida.append(f'<h{n} class="mt-10 mb-4 font-display {tam} font-extrabold '
                         f'tracking-tight text-ink-900">{inline(m.group(2))}</h{n}>')
            i += 1
            continue

        if re.match(r'^[-*]\s+', cru):
            itens = []
            while i < len(linhas) and re.match(r'^[-*]\s+', linhas[i].strip()):
                itens.append(inline(re.sub(r'^[-*]\s+', '', linhas[i].strip())))
                i += 1
            lis = ''.join(f'<li class="pl-1">{t}</li>' for t in itens)
            saida.append(f'<ul class="mb-5 ml-5 list-disc space-y-2 text-ink-800 marker:text-rose-500">{lis}</ul>')
            continue

        if re.match(r'^\d+\.\s+', cru):
            itens = []
            while i < len(linhas) and re.match(r'^\d+\.\s+', linhas[i].strip()):
                itens.append(inline(re.sub(r'^\d+\.\s+', '', linhas[i].strip())))
                i += 1
            lis = ''.join(f'<li class="pl-1">{t}</li>' for t in itens)
            saida.append(f'<ol class="mb-5 ml-5 list-decimal space-y-2 text-ink-800 marker:font-bold '
                         f'marker:text-rose-500">{lis}</ol>')
            continue

        # parágrafo: junta linhas até a próxima linha em branco
        bloco = []
        while i < len(linhas) and linhas[i].strip() and not re.match(
                r'^(#{1,6}\s|[-*]\s|\d+\.\s|\||>)', linhas[i].strip()):
            bloco.append(linhas[i].strip())
            i += 1
        if bloco:
            saida.append(f'<p class="mb-5 leading-relaxed text-ink-800">{inline(" ".join(bloco))}</p>')

    return '\n'.join(saida)


def frontmatter(texto: str) -> tuple[dict, str]:
    """Separa o frontmatter YAML do corpo. Parser mínimo, sem dependência."""
    if not texto.startswith('---'):
        return {}, texto
    fim = texto.index('\n---', 3)
    bruto, corpo = texto[3:fim], texto[fim + 4:]

    dados: dict = {}
    chave_lista = None
    for linha in bruto.split('\n'):
        if not linha.strip() or linha.strip().startswith('#'):
            continue
        if re.match(r'^\s+-\s', linha) and chave_lista:
            dados[chave_lista].append(linha.strip()[2:].strip().strip('"\''))
            continue
        m = re.match(r'^([A-Za-z_][\w]*):\s*(.*)$', linha)
        if not m:
            continue
        chave, valor = m.group(1), m.group(2).strip()
        if valor == '':
            dados[chave] = []
            chave_lista = chave
        else:
            chave_lista = None
            v = valor.strip('"\'')
            if v in ('true', 'false'):
                dados[chave] = (v == 'true')
            elif re.fullmatch(r'-?\d+', v):
                dados[chave] = int(v)
            else:
                dados[chave] = v
    return dados, corpo.lstrip('\n')


def secoes(corpo: str) -> list[tuple[str, str]]:
    """Quebra o corpo em (título de nível 2, conteúdo). O texto antes do
    primeiro `##` volta com título vazio."""
    partes = re.split(r'^## +(.+)$', corpo, flags=re.M)
    resultado = [('', partes[0])]
    for i in range(1, len(partes), 2):
        resultado.append((partes[i].strip(), partes[i + 1]))
    return resultado
