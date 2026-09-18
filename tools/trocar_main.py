#!/usr/bin/env python3
"""Troca a região <main> de uma página, preservando o chrome.

    python3 tools/trocar_main.py <pagina.html> <corpo.html>

O chrome (head, header, footer) é responsabilidade do sync_chrome.py; este
script só encosta no miolo, delimitado por <main ...> e <footer.
"""
import re
import sys


def main() -> int:
    pagina, corpo_novo = sys.argv[1], sys.argv[2]
    with open(corpo_novo, encoding='utf-8') as fh:
        novo = fh.read().rstrip('\n') + '\n'
    with open(pagina, encoding='utf-8') as fh:
        txt = fh.read()

    ini = re.search(r'^<main', txt, re.M)
    fim = re.search(r'^<footer', txt, re.M)
    if not (ini and fim):
        print(f'ERRO: {pagina} não tem <main> ou <footer> no início de linha')
        return 1

    with open(pagina, 'w', encoding='utf-8') as fh:
        fh.write(txt[:ini.start()] + novo + txt[fim.start():])
    print(f'  {pagina}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
