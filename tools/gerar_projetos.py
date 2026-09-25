#!/usr/bin/env python3
"""Gera as 8 páginas de projeto a partir dos markdowns de conteúdo.

Fonte: informacoes/conteudo/projetos/*.md (frontmatter + corpo).
Saída: site-v1/projetos/<slug>.html

O chrome (head/header/footer) é escrito depois por sync_chrome.py, que é a
fonte única dele. Este script cuida só do miolo da página.

Seções do markdown que NÃO vão para o site: "Fotos", "Depoimento" e
"Dados estruturados" — são notas de produção. O JSON-LD é extraído da última
e injetado como <script type="application/ld+json">.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md as MD  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTEUDO = os.path.normpath(os.path.join(RAIZ, '..', 'informacoes', 'conteudo', 'projetos'))
SAIDA = os.path.join(RAIZ, 'projetos')

NAO_PUBLICAR = {'Fotos', 'Depoimento', 'Dados estruturados', 'Pendências',
                'Pendências de conteúdo', 'Nota de implementação'}

# Cor por eixo, não por projeto: reforça a leitura de categoria na listagem.
# `gold` fica fora de propósito — é a cor de doação e do selo "a confirmar".
EIXOS = {
    'Arte e cultura': 'rose',
    'Educação e aprendizagem': 'sky',
    'Esporte e inclusão': 'verde',
    'Convivência e protagonismo': 'laranja',
    'Convivência comunitária': 'laranja',
}

# Galeria por projeto. A primeira é a de abertura; as demais entram na grade.
# Só entram fotos com descrição verificada em 09-metadados-imagens.md.
GALERIAS = {
    'o-som-do-bem': [
        ('oficina-de-canto/canto-01.webp',
         'Crianças com camiseta do SECRI reunidas sob o painel do Recital de Canto Coral',
         'Educandos do SECRI no Recital de Flauta, Canto e Libras'),
        ('o-som-do-bem/o-som-do-bem-03.webp',
         'Turma do projeto O Som do Bem desenhando instrumentos musicais em sala com mural de mapa-múndi',
         'Atividade de desenho sobre instrumentos musicais'),
        ('o-som-do-bem/o-som-do-bem-04.webp',
         'Dois meninos de camiseta azul-clara desenhando juntos na biblioteca do SECRI',
         'Atividade de desenho sobre instrumentos musicais'),
        ('o-som-do-bem/o-som-do-bem-01.webp',
         'Duas meninas colorindo desenhos de instrumentos musicais em mesa cheia de lápis de cor',
         'Atividade de desenho sobre instrumentos musicais'),
    ],
    'oficina-de-canto': [
        ('oficina-de-canto/canto-01.webp',
         'Coral de cerca de 30 crianças com camiseta do SECRI posando sob o painel Recital Canto Coral',
         'O coral do SECRI no Recital de Canto Coral'),
    ],
    'engajando-futuros': [
        ('engajando-futuros/engajando-futuros-01-social.webp',
         'Roda de conversa do grupo Engajando Futuros na biblioteca do SECRI, com adolescentes '
         'sentados em círculo e duas educadoras conduzindo',
         'Roda de conversa do grupo Engajando Futuros'),
    ],
    'travessia': [
        ('travessia/travessia-03.webp',
         'Turma de bailarinas do Projeto Travessia com os braços em quinta posição, espalhadas '
         'pelo salão de dança da Academia Duetto',
         'Aula do Projeto Travessia na Academia Duetto'),
        ('travessia/travessia-02.webp',
         'Bailarinas do Projeto Travessia em posição de ballet clássico, de collant preto',
         'Bailarinas em aula na Academia Duetto'),
    ],
    'inova-bem': [
        ('inova-bem/inova-bem-turma-estudando-tablets.webp',
         'Turma do Inova Bem estudando em mesa coletiva, cada estudante com tablet, teclado e fone de ouvido',
         'Turma do Inova Bem em aula'),
        ('inova-bem/inova-bem-estudante-escrevendo-caderno.webp',
         'Estudante do Inova Bem escrevendo no caderno durante aula online, com educadora acompanhando ao fundo',
         'Aula personalizada com acompanhamento presencial'),
        ('inova-bem/inova-bem-aula-geometria-videochamada-anonimizada.webp',
         'Estudante resolvendo exercício de geometria no caderno enquanto acompanha a professora '
         'por videochamada no tablet',
         'Exercício de geometria acompanhado por videochamada'),
    ],
    'canoa-viva': [
        ('canoa-viva/canoa-02.webp',
         'Adolescentes carregando juntos a canoa havaiana Benedito sobre a cabeça, atravessando a areia da praia',
         'Adolescentes levando a canoa Benedito para a água'),
        ('canoa-viva/canoa-01.webp',
         'Grupo de adolescentes do projeto Canoa Viva remando em canoa havaiana na Praia da Guarderia, '
         'em Vitória, com veleiros ancorados ao fundo',
         'Treino na Praia da Guarderia, em Vitória'),
        ('canoa-viva/canoa-05.webp',
         'Três adolescentes sentados na canoa com colete salva-vidas e remo em punho, recebendo '
         'orientação do instrutor',
         'Orientação antes de entrar na água'),
        ('canoa-viva/canoa-06.webp',
         "Turma do Canoa Viva embarcando na canoa dentro d'água, acompanhada por dois educadores",
         'Embarque acompanhado pelos educadores'),
    ],
    'judo': [
        ('judo/judo-02.webp',
         'Professora de quimono e faixa preta corrigindo a pegada de dois meninos em pé no tatame, '
         'com a turma sentada ao fundo',
         'Aula de judô no tatame da sede'),
        ('judo/judo-01.webp',
         'Crianças treinando judô em duplas sobre tatame azul, acompanhadas pela professora de '
         'quimono e faixa preta',
         'Treino em duplas'),
    ],
    'movimento-com-qualidade-de-vida': [
        ('movimento-com-qualidade-de-vida/mov-qualid-de-vida-01.webp',
         'Grupo de adultos com mais de 50 anos fazendo exercício de agachamento com apoio de cadeira, '
         'orientados por um educador físico',
         'Atividade física orientada por educador físico'),
        ('movimento-com-qualidade-de-vida/mov-qualid-de-vida-02.webp',
         'Roda de mulheres em volta da mesa em oficina de bordado, com peças bordadas em rosa e azul '
         'expostas à frente',
         'Oficina de bordado do grupo'),
    ],
}


def esc(t: str) -> str:
    return html.escape(t, quote=True)


def resolve_links(html_txt: str, na_raiz: bool) -> str:
    """Os markdowns linkam projetos como `/projetos/<slug>`, que é a URL final.
    O site é aberto direto do disco, então vira caminho relativo com .html."""
    destino = r'href="projetos/\1.html"' if na_raiz else r'href="\1.html"'
    return re.sub(r'href="/projetos/([a-z0-9-]+)/?"', destino, html_txt)


# Quem banca e quem executa são papéis diferentes, então a página separa os
# dois. `logo` vazio renderiza uma caixa nomeada avisando que o arquivo ainda
# precisa ser conseguido — mesma lógica da faixa de parceiros da home.
PARCEIROS = {
 'o-som-do-bem': {
   'patrocinio': [('ArcelorMittal Tubarão', 'arcelormittal.png',
                   'Aprovado em seleção pública no edital ArcelorMittal Investe')],
   'apoio': [],
 },
 'oficina-de-canto': {
   'patrocinio': [('SETADES - Secretaria de Trabalho, Assistência e Desenvolvimento Social', '',
                   'Termo de Fomento nº 052/2024 - D7JCM')],
   'apoio': [('SCFV - Serviço de Convivência e Fortalecimento de Vínculos', 'scfv.png',
              'A oficina é ofertada dentro do SCFV')],
 },
 'engajando-futuros': {
   'patrocinio': [('SETADES - Secretaria de Trabalho, Assistência e Desenvolvimento Social', '',
                   'Termo de Fomento nº 052/2024 - D7JCM')],
   'apoio': [('SCFV - Serviço de Convivência e Fortalecimento de Vínculos', 'scfv.png',
              'O grupo é ofertado dentro do SCFV'),
             ('UFES - Engenharia Elétrica', '',
              'Minicurso Saberes Tecnológicos e projeto Pequenos Cientistas')],
 },
 'travessia': {
   'patrocinio': [('ArcelorMittal', 'arcelormittal.png',
                   'Viabilizou o espetáculo Ballerina, na Casa da Música Sônia Cabral')],
   'apoio': [('Mover-se Cia de Dança', '', 'Execução do projeto'),
             ('Academia Duetto Arte e Movimento', '', 'Cede o espaço e a estrutura técnica'),
             ('Marcelo Lages', '', 'Apoio ao projeto')],
 },
 'inova-bem': {
   'patrocinio': [],
   'apoio': [('Luma - Ensino Personalizado', '', 'Metodologia e execução das aulas')],
 },
 'canoa-viva': {
   'patrocinio': [('Vale', '', 'Recursos da Lei de Incentivo ao Esporte'),
                  ('Ministério do Esporte', '', 'Lei de Incentivo ao Esporte'),
                  ('Estel', '', ''),
                  ('timenow', '', '')],
   'apoio': [('Instituto Maratonas', 'canoa-viva.png',
              'Executa a atividade e disponibiliza canoas, equipamentos e instrutores')],
 },
 'judo': {
   'patrocinio': [],
   'apoio': [('Instituto Maratonas', '', 'Executa a atividade')],
 },
 'movimento-com-qualidade-de-vida': {
   'patrocinio': [],
   'apoio': [],
 },
}


def cartao_parceiro(nome: str, logo: str, detalhe: str) -> str:
    if logo:
        visual = (f'<img src="../assets/parceiros/{logo}" alt="{esc(nome)}" loading="lazy" '
                  f'decoding="async" width="600" height="240" class="max-h-16 w-auto">')
        moldura = 'bg-white ring-1 ring-ink-200'
    else:
        # o nome já aparece como legenda logo abaixo da caixa; repeti-lo aqui
        # dentro deixaria a mesma palavra duas vezes coladas
        visual = '<span class="text-center text-xs text-ink-400">logo a buscar</span>'
        moldura = 'border-2 border-dashed border-ink-300 bg-white'
    legenda = (f'<p class="mt-2 text-xs leading-relaxed text-ink-600">{MD.inline(detalhe)}</p>'
               if detalhe else '')
    return (f'<div><div class="flex h-20 items-center justify-center rounded-xl p-3 {moldura}">'
            f'{visual}</div>'
            f'<p class="mt-2 text-sm font-semibold text-ink-900">{esc(nome)}</p>{legenda}</div>')


def blocos_parceiros(slug: str, cor: str) -> str:
    dados = PARCEIROS.get(slug, {})
    partes = []
    for chave, titulo, explica in [
            ('patrocinio', 'Patrocínio', 'Quem financia o projeto'),
            ('apoio', 'Apoio', 'Quem executa e sustenta a atividade')]:
        itens = dados.get(chave, [])
        if not itens:
            continue
        cartoes = ''.join(cartao_parceiro(*i) for i in itens)
        partes.append(f"""
  <div class="mt-8">
    <h2 class="font-display text-sm font-bold uppercase tracking-wide text-{cor}-700">{titulo}</h2>
    <p class="mb-4 text-xs text-ink-600">{explica}</p>
    <div class="grid gap-4 sm:grid-cols-2">{cartoes}</div>
  </div>""")
    if not partes:
        return ('\n  <div class="mt-8 rounded-2xl border border-gold-300 bg-gold-50 p-5">'
                '<p class="text-sm leading-relaxed text-ink-800">'
                '<strong class="font-bold">Patrocínio e apoio:</strong> '
                '<span class="inline-flex items-center gap-1 rounded-full bg-gold-100 px-2.5 py-0.5 '
                'text-xs font-bold uppercase tracking-wide text-gold-700 ring-1 ring-gold-300">'
                'a confirmar</span></p></div>')
    return ''.join(partes)


def caixa_pendencias(fm: dict) -> str:
    if not fm.get('pendencias'):
        return ''
    itens = ''.join(f'<li>{MD.inline(p)}</li>' for p in fm['pendencias'])
    n = len(fm['pendencias'])
    plural = 'informação' if n == 1 else 'informações'
    return f'''
  <div role="note" class="mb-10 rounded-2xl border border-gold-300 bg-gold-50 p-5 sm:p-6">
    <p class="mb-2 flex items-center gap-2 font-display text-sm font-extrabold uppercase tracking-wide text-gold-700">
      <span aria-hidden="true">●</span> Página em validação
    </p>
    <p class="mb-3 text-sm leading-relaxed text-ink-800">
      Esta página tem <strong class="font-bold">{n} {plural}</strong> que o SECRI ainda precisa confirmar.
      Os trechos marcados no texto aparecem abaixo:
    </p>
    <ul class="ml-5 list-disc space-y-1 text-sm text-ink-800 marker:text-gold-700">{itens}</ul>
  </div>'''


def ficha_tecnica(fm: dict, cor: str) -> str:
    # Faixa etária e custo saíram da ficha a pedido do cliente. A gratuidade
    # continua dita no texto de abertura e na FAQ de cada projeto.
    campos = [('Público', fm.get('publico')),
              ('Onde acontece', fm.get('local')),
              ('Frequência', fm.get('frequencia'))]
    linhas = []
    for rotulo, valor in campos:
        if not valor:
            continue
        linhas.append(
            f'<div class="border-t border-ink-200 py-3">'
            f'<dt class="font-display text-xs font-bold uppercase tracking-wide text-ink-600">{esc(rotulo)}</dt>'
            f'<dd class="mt-1 text-ink-900">{MD.inline(str(valor))}</dd></div>')
    return (f'<dl class="rounded-2xl border-t-4 border-{cor}-500 bg-ink-50 px-5 py-2 sm:px-6">'
            + ''.join(linhas) + '</dl>')


def galeria(slug: str, cor: str) -> str:
    fotos = GALERIAS.get(slug, [])[1:]
    if not fotos:
        return ''
    cels = []
    for arq, alt, legenda in fotos:
        cels.append(f'''
      <figure class="overflow-hidden rounded-2xl bg-ink-50 ring-1 ring-ink-200">
        <img src="../assets/fotos/{arq}" alt="{esc(alt)}" loading="lazy" decoding="async"
             class="h-56 w-full object-cover sm:h-64">
        <figcaption class="px-4 py-3 text-xs leading-relaxed text-ink-600">{esc(legenda)}</figcaption>
      </figure>''')
    return f'''
  <section class="mt-14">
    <h2 class="mb-6 font-display text-2xl font-extrabold tracking-tight text-ink-900 sm:text-3xl">
      O projeto em imagens
    </h2>
    <div class="grid gap-5 sm:grid-cols-2">{''.join(cels)}</div>
  </section>'''


def faq_para_html(bruto: str) -> tuple[str, list[tuple[str, str]]]:
    """A FAQ vem como pares de linhas: pergunta em negrito, resposta abaixo."""
    pares: list[tuple[str, str]] = []
    linhas = [l.strip() for l in bruto.split('\n')]
    i = 0
    while i < len(linhas):
        m = re.match(r'^\*\*(.+?)\*\*$', linhas[i])
        if m:
            pergunta = m.group(1)
            resp = []
            i += 1
            while i < len(linhas) and linhas[i] and not linhas[i].startswith('**'):
                resp.append(linhas[i])
                i += 1
            pares.append((pergunta, ' '.join(resp)))
        else:
            i += 1
    itens = ''.join(f'''
      <details class="group border-t border-ink-200 py-4">
        <summary class="flex cursor-pointer list-none items-center justify-between gap-4 font-display
                        font-bold text-ink-900 marker:hidden">
          {MD.inline(p)}
          <span aria-hidden="true" class="text-xl text-ink-400 transition-transform group-open:rotate-45">+</span>
        </summary>
        <div class="mt-3 leading-relaxed text-ink-800">{MD.inline(r)}</div>
      </details>''' for p, r in pares)
    return itens, pares


def json_ld(corpo: str, slug: str, fm: dict) -> str:
    m = re.search(r'```json\s*(\{.*?\})\s*```', corpo, re.S)
    blocos = []
    if m:
        try:
            dados = json.loads(m.group(1))
            dados['url'] = f'https://secri.org.br/projetos/{slug}.html'
            blocos.append(dados)
        except json.JSONDecodeError:
            pass
    blocos.append({
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': 'https://secri.org.br/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Projetos',
             'item': 'https://secri.org.br/projetos.html'},
            {'@type': 'ListItem', 'position': 3, 'name': fm['titulo'],
             'item': f'https://secri.org.br/projetos/{slug}.html'},
        ]})
    return '\n'.join(
        '<script type="application/ld+json">\n'
        + json.dumps(b, ensure_ascii=False, indent=2) + '\n</script>' for b in blocos)


def gera(caminho_md: str) -> tuple[str, dict]:
    with open(caminho_md, encoding='utf-8') as fh:
        fm, corpo = MD.frontmatter(fh.read())

    slug = fm['slug']
    cor = EIXOS.get(fm.get('eixo', ''), 'rose')
    fotos = GALERIAS.get(slug, [])
    hero = fotos[0] if fotos else None

    selo = ''
    if fm.get('selo'):
        selo = (f'<span class="ml-3 inline-flex items-center rounded-full bg-{cor}-500 px-3 py-1 '
                f'align-middle text-sm font-bold text-white">{esc(str(fm["selo"]))}</span>')

    corpo_html, faq_html, faq_pares = [], '', []
    for titulo, trecho in MD.secoes(corpo):
        if not titulo:
            continue
        if titulo in NAO_PUBLICAR:
            continue
        if titulo == 'Perguntas frequentes':
            faq_html, faq_pares = faq_para_html(trecho)
            continue
        if titulo == 'Para quem é':
            # a ficha técnica já mostra esses dados; aqui fica só a prosa
            prosa = '\n'.join(l for l in trecho.split('\n') if not re.match(r'^\*\*\w', l.strip()))
            corpo_html.append(f'<h2 class="mt-10 mb-4 font-display text-2xl font-extrabold '
                              f'tracking-tight text-ink-900 sm:text-3xl">{esc(titulo)}</h2>')
            corpo_html.append(MD.render(prosa))
            continue
        corpo_html.append(f'<h2 class="mt-10 mb-4 font-display text-2xl font-extrabold '
                          f'tracking-tight text-ink-900 sm:text-3xl">{esc(titulo)}</h2>')
        corpo_html.append(MD.render(trecho))

    if faq_pares:
        fld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': re.sub(r'[*`]', '', p),
             'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'[*`\[\]]|\(https?://[^)]+\)', '', r)}}
            for p, r in faq_pares]}
        faq_ld = ('<script type="application/ld+json">\n'
                  + json.dumps(fld, ensure_ascii=False, indent=2) + '\n</script>')
    else:
        faq_ld = ''

    hero_html = ''
    if hero:
        arq, alt, legenda = hero
        hero_html = f'''
  <figure class="mb-10 overflow-hidden rounded-3xl bg-ink-50 ring-1 ring-ink-200">
    <img src="../assets/fotos/{arq}" alt="{esc(alt)}" fetchpriority="high" decoding="async"
         class="h-64 w-full object-cover sm:h-80 lg:h-[420px]">
    <figcaption class="px-5 py-3 text-xs leading-relaxed text-ink-600">{esc(legenda)}</figcaption>
  </figure>'''

    faq_secao = f'''
  <section class="mt-14">
    <h2 class="mb-2 font-display text-2xl font-extrabold tracking-tight text-ink-900 sm:text-3xl">
      Perguntas frequentes
    </h2>
    <div class="mt-6">{faq_html}</div>
  </section>''' if faq_html else ''

    main = f'''<main id="conteudo">

  <nav aria-label="Trilha de navegação" class="border-b border-ink-200 bg-ink-50 px-4 py-3 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-5xl text-sm text-ink-600">
      <a href="../index.html" class="hover:text-rose-700">Início</a>
      <span aria-hidden="true" class="mx-2 text-ink-300">/</span>
      <a href="../projetos.html" class="hover:text-rose-700">Projetos</a>
      <span aria-hidden="true" class="mx-2 text-ink-300">/</span>
      <span class="text-ink-900">{esc(fm['titulo'])}</span>
    </div>
  </nav>

  <section class="bg-ink-50 px-4 py-12 text-center sm:py-16 lg:py-20">
    <div class="mx-auto max-w-3xl">
      <span class="mb-4 inline-block rounded-full bg-{cor}-100 px-4 py-2 text-xs font-bold
                   uppercase tracking-wide text-{cor}-700 sm:text-sm">{esc(fm.get('categoria', ''))}</span>
      <h1 class="mb-5 font-display text-3xl font-extrabold leading-tight tracking-tight text-ink-900
                 sm:text-4xl lg:text-5xl">{esc(fm['titulo'])}{selo}</h1>
      <p class="text-base leading-relaxed text-ink-600 sm:text-lg">{esc(fm.get('subtitulo', ''))}</p>
    </div>
  </section>

  <div class="mx-auto max-w-5xl px-4 py-12 sm:px-6 sm:py-16 lg:px-8">
{caixa_pendencias(fm)}
{hero_html}

    <div class="grid gap-10 lg:grid-cols-[1fr_20rem] lg:gap-14">
      <div>
{chr(10).join(corpo_html)}
      </div>
      <aside class="lg:pt-10">
        <h2 class="mb-4 font-display text-sm font-bold uppercase tracking-wide text-ink-600">Ficha técnica</h2>
        {ficha_tecnica(fm, cor)}
        {blocos_parceiros(slug, cor)}
      </aside>
    </div>
{galeria(slug, cor)}
{faq_secao}

    <section class="mt-16 rounded-3xl bg-{cor}-50 px-6 py-10 text-center ring-1 ring-{cor}-300 sm:px-10">
      <h2 class="mb-3 font-display text-2xl font-extrabold tracking-tight text-ink-900 sm:text-3xl">
        Quer apoiar este projeto?
      </h2>
      <p class="mx-auto mb-7 max-w-xl leading-relaxed text-ink-800">
        Projetos como este existem porque pessoas e empresas decidiram apoiá-los.
      </p>
      <div class="flex flex-col justify-center gap-3 sm:flex-row sm:gap-4">
        <a href="../doe.html"
           class="inline-flex items-center justify-center rounded-full bg-gold-500 px-7 py-3 text-sm
                  font-bold text-ink-900 transition-colors hover:bg-gold-300 focus-visible:outline
                  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink-900
                  sm:text-base">Quero doar</a>
        <a href="../projetos.html"
           class="inline-flex items-center justify-center rounded-full border-2 border-ink-300 px-7 py-3
                  text-sm font-bold text-ink-900 transition-colors hover:border-{cor}-500
                  hover:text-{cor}-700 sm:text-base">Ver os outros projetos</a>
      </div>
    </section>
  </div>
{json_ld(corpo, slug, fm)}
{faq_ld}
</main>
'''
    return main, fm


# A abertura do Som do Bem e a única foto da Oficina de Canto são a mesma
# imagem. Na listagem os dois cards ficariam idênticos lado a lado, então o
# card do Som do Bem usa outra foto.
CARD_FOTO = {'o-som-do-bem': 1}

ORDEM_EIXOS = ['Arte e cultura', 'Educação e aprendizagem', 'Esporte e inclusão',
               'Convivência e bem-estar']

# Os markdowns trazem dois rótulos de convivência; na listagem eles formam
# uma seção só, já que dividem a mesma cor de eixo.
FUNDE_EIXO = {'Convivência e protagonismo': 'Convivência e bem-estar',
              'Convivência comunitária': 'Convivência e bem-estar'}


def gera_listagem(projetos: list[dict]) -> str:
    """Monta projetos.html agrupando os cards por eixo."""
    md_index = os.path.join(CONTEUDO, '_index-projetos.md')
    with open(md_index, encoding='utf-8') as fh:
        fm_idx, corpo_idx = MD.frontmatter(fh.read())

    faq_html, faq_pares = '', []
    intro = ''
    for titulo, trecho in MD.secoes(corpo_idx):
        if titulo == 'Perguntas frequentes':
            faq_html, faq_pares = faq_para_html(trecho)
        elif titulo == '':
            intro = MD.render(re.sub(r'^# .*$', '', trecho, flags=re.M))

    grupos: dict[str, list[dict]] = {}
    for p in projetos:
        eixo = p['fm'].get('eixo', 'Outros')
        grupos.setdefault(FUNDE_EIXO.get(eixo, eixo), []).append(p)

    blocos = []
    for eixo in ORDEM_EIXOS + [e for e in grupos if e not in ORDEM_EIXOS]:
        if eixo not in grupos:
            continue
        cartoes = []
        for p in sorted(grupos[eixo], key=lambda x: x['fm'].get('ordem', 99)):
            fm, slug = p['fm'], p['fm']['slug']
            cor = EIXOS.get(fm.get('eixo', ''), 'rose')
            fotos = GALERIAS.get(slug, [])
            idx = CARD_FOTO.get(slug, 0)
            arq, alt, _ = fotos[idx] if len(fotos) > idx else fotos[0]
            n_pend = len(fm.get('pendencias', []))
            selo = (f'<span class="ml-2 inline-flex items-center rounded-full bg-{cor}-500 px-2.5 '
                    f'py-0.5 text-xs font-bold text-white">{esc(str(fm["selo"]))}</span>'
                    if fm.get('selo') else '')
            aviso = (f'<span class="mt-3 self-start inline-flex items-center gap-1 rounded-full bg-gold-100 '
                     f'px-2.5 py-0.5 text-xs font-bold text-gold-700 ring-1 ring-gold-300">'
                     f'{n_pend} a confirmar</span>' if n_pend else '')
            cartoes.append(f'''
        <a href="projetos/{slug}.html"
           class="group flex flex-col overflow-hidden rounded-2xl border-t-4 border-{cor}-500 bg-white
                  shadow-sm ring-1 ring-ink-200 transition-transform hover:-translate-y-1">
          <img src="assets/fotos/{arq}" alt="{esc(alt)}" loading="lazy" decoding="async"
               class="h-44 w-full object-cover">
          <div class="flex flex-grow flex-col p-6">
            <h3 class="mb-2 font-display text-lg font-bold text-ink-900 sm:text-xl">{esc(fm['titulo'])}{selo}</h3>
            <p class="mb-4 flex-grow text-sm leading-relaxed text-ink-600">{esc(fm.get('subtitulo', ''))}</p>
            <p class="text-xs text-ink-600">Parceria: <span class="font-semibold">{MD.inline(str(fm.get('parceiro', '')))}</span></p>
            {aviso}
            <span class="mt-4 text-sm font-bold text-{cor}-700">Conhecer o projeto &rarr;</span>
          </div>
        </a>''')
        blocos.append(f'''
    <section class="mt-14 first:mt-0">
      <h2 class="mb-6 font-display text-xl font-extrabold tracking-tight text-ink-900 sm:text-2xl">{esc(eixo)}</h2>
      <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{''.join(cartoes)}</div>
    </section>''')

    faq_secao = f'''
    <section class="mt-16">
      <h2 class="mb-6 font-display text-2xl font-extrabold tracking-tight text-ink-900 sm:text-3xl">
        Perguntas frequentes
      </h2>
      {faq_html}
    </section>''' if faq_html else ''

    fld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': re.sub(r'[*`]', '', p),
         'acceptedAnswer': {'@type': 'Answer',
                            'text': re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', re.sub(r'[*`]', '', r))}}
        for p, r in faq_pares]}

    return f'''<main id="conteudo">

  <section class="bg-ink-50 px-4 py-12 text-center sm:py-16 lg:py-20">
    <div class="mx-auto max-w-3xl">
      <h1 class="mb-5 font-display text-3xl font-extrabold leading-tight tracking-tight text-ink-900
                 sm:text-4xl lg:text-5xl">Nossos Projetos</h1>
      <p class="text-base leading-relaxed text-ink-600 sm:text-lg">{esc(fm_idx.get('subtitulo', ''))}</p>
    </div>
  </section>

  <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 sm:py-16 lg:px-8">
    <div class="mx-auto max-w-3xl">{intro}</div>
{''.join(blocos)}
{faq_secao}
  </div>
<script type="application/ld+json">
{json.dumps(fld, ensure_ascii=False, indent=2)}
</script>
</main>
'''


def main() -> int:
    os.makedirs(SAIDA, exist_ok=True)
    registro = {}
    arquivos = sorted(f for f in os.listdir(CONTEUDO)
                      if f.endswith('.md') and not f.startswith(('_', 'README')))

    def esqueleto(corpo: str) -> str:
        """Chrome vazio; sync_chrome.py preenche head, header e footer depois."""
        return ('<!doctype html>\n<html lang="pt-BR">\n<head>\n</head>\n'
                '<body class="bg-white font-sans text-ink-900 antialiased">\n'
                + corpo + '<footer></footer>\n</body>\n</html>\n')

    projetos = []
    for nome in arquivos:
        corpo, fm = gera(os.path.join(CONTEUDO, nome))
        with open(os.path.join(SAIDA, f'{fm["slug"]}.html'), 'w', encoding='utf-8') as fh:
            fh.write(esqueleto(resolve_links(corpo, na_raiz=False)))
        projetos.append({'fm': fm})
        registro[f'projetos/{fm["slug"]}.html'] = {
            'nav': 'projetos',
            'title': fm.get('seo_title', f'SECRI — {fm["titulo"]}'),
            'description': fm.get('meta_description', ''),
        }
        print(f'  {fm["slug"]+".html":40} {len(fm.get("pendencias", [])):>2} pendências  '
              f'eixo={EIXOS.get(fm.get("eixo",""), "rose")}')

    with open(os.path.join(CONTEUDO, '_index-projetos.md'), encoding='utf-8') as fh:
        fm_idx, _ = MD.frontmatter(fh.read())
    with open(os.path.join(RAIZ, 'projetos.html'), 'w', encoding='utf-8') as fh:
        fh.write(esqueleto(resolve_links(gera_listagem(projetos), na_raiz=True)))
    registro['projetos.html'] = {
        'nav': 'projetos',
        'title': fm_idx.get('seo_title', 'SECRI — Projetos'),
        'description': fm_idx.get('meta_description', ''),
    }
    print(f'  {"projetos.html":40} {len(fm_idx.get("pendencias", [])):>2} pendências  (listagem)')

    with open(os.path.join(RAIZ, 'tools', 'projetos.gerado.json'), 'w', encoding='utf-8') as fh:
        json.dump(registro, fh, ensure_ascii=False, indent=2)
    print(f'\n{len(arquivos)} páginas de projeto + listagem')
    return 0


if __name__ == '__main__':
    sys.exit(main())
