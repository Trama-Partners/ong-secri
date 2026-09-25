# CLAUDE.md — site do SECRI

Site institucional do **SECRI - Serviço de Engajamento Comunitário**, Vitória/ES.
HTML estático puro, sem build. Abre direto do disco.

---

## ⚠️ Regra permanente: toda alteração relevante exige acertar o SEO

O SEO deste site não é um arquivo isolado — está espalhado em metadados, dados
estruturados e sitemap, todos derivados de `tools/site.json`. **Mexeu no
conteúdo, rode a cadeia de SEO antes de encerrar.**

| Se você alterou… | Precisa fazer |
|---|---|
| Texto de uma página | Revisar `title` e `description` em `tools/site.json` · `sync_chrome.py --apply` |
| Criou ou removeu página | Registrar/remover em `tools/site.json` (com `schema` e `breadcrumb`) · `sync_chrome.py --apply` · `gerar_seo.py` |
| Renomeou arquivo ou mudou URL | Atualizar `site.json` · rodar os dois scripts · conferir se algum link interno quebrou |
| Trocou ou adicionou foto | `gerar_seo.py` (o sitemap de imagens lê o HTML) · conferir `alt` · se for foto de abertura, regerar o `og:image` |
| Mudou nome, telefone, CNPJ ou endereço | `tools/partials/footer.html` e `site.json` · conferir o JSON-LD, que repete esses dados |
| Editou markdown de projeto | `gerar_projetos.py` · `sync_chrome.py --apply` · `gerar_seo.py` · `gerar_llms.py` |
| Qualquer alteração de texto publicado | `gerar_llms.py` — o `llms-full.txt` é cópia do conteúdo e desatualiza calado |

**Cadeia completa, na ordem:**

```bash
python3 tools/gerar_projetos.py      # páginas de projeto + listagem
python3 tools/sync_chrome.py --apply  # head, header, footer, meta tags, JSON-LD
python3 tools/gerar_seo.py            # sitemap.xml + robots.txt
python3 tools/gerar_llms.py           # llms.txt + llms-full.txt
```

Rodar fora de ordem não quebra nada, mas `gerar_seo.py` e `gerar_llms.py` leem o
HTML final — então vêm por último, senão o sitemap e o conteúdo para IA saem
defasados.

---

## O que já está configurado

**Por página, gerado de `tools/site.json`:**
`<title>` único (≤ 60 caracteres) · `meta description` (120–160) · `canonical` ·
Open Graph completo (`type`, `site_name`, `locale`, `title`, `description`,
`url`, `image`, `image:alt`, `image:width`, `image:height`) · Twitter Card
`summary_large_image` com `image:alt` · `theme-color` · favicon SVG + PNG 32 ·
apple-touch-icon · `site.webmanifest` · `noindex` nas páginas internas.

**Dados estruturados (JSON-LD):**

| Página | Tipos |
|---|---|
| index | `WebPage` + `NGO` (CNPJ, endereço, telefones, sameAs) |
| quem-somos | `AboutPage` + `BreadcrumbList` |
| projetos | `CollectionPage` + `FAQPage` + `BreadcrumbList` |
| cada projeto | `Course`, `SportsActivityLocation` ou `Service` + `BreadcrumbList` + `FAQPage` |
| contato | `ContactPage` + `NGO` com dois `ContactPoint` |
| demais | `WebPage` + `BreadcrumbList` |

**Arquivos na raiz:** `sitemap.xml` (18 URLs, 47 imagens, `lastmod` real dos
arquivos), `robots.txt`, `site.webmanifest`, `404.html`.

**Imagens:** todas com `alt` preenchido, `width`/`height` explícitos (evita
salto de layout, que o Google mede), `loading="lazy"` fora da dobra e
`fetchpriority="high"` no hero. Nenhuma acima de 300 KB. Imagens de
compartilhamento em `assets/og/`, recortadas em 1200×630 — servir retrato faz o
card cortar no lugar errado.

---

## Indexação por sistemas de IA

Buscador tradicional rastreia HTML; assistente de IA trabalha melhor com
markdown limpo. Sem isso a IA precisa interpretar marcação Tailwind e costuma
resumir errado.

**Arquivos na raiz, gerados por `tools/gerar_llms.py`:**

- `llms.txt` — índice: resumo da instituição, números de 2025, uma linha por
  página com descrição, dados de contato e um aviso de que a versão está em
  validação (para a IA não citar como fato o que está "a confirmar")
- `llms-full.txt` — texto integral das 18 páginas em um arquivo, ~50 KB, com
  comentário `<!-- fonte: URL -->` antes de cada uma para a IA saber citar

**Política de crawlers no `robots.txt`**, definida em `tools/gerar_seo.py`:

| Grupo | Bots | Regra |
|---|---|---|
| Resposta | OAI-SearchBot, ChatGPT-User, Claude-User, Claude-SearchBot, PerplexityBot, Perplexity-User, Gemini-Deep-Research, DuckAssistBot, MistralAI-User, YouBot | liberado |
| Treinamento | GPTBot, ClaudeBot, Google-Extended, CCBot, Bytespider, Meta-ExternalAgent, Applebot-Extended, Amazonbot, Diffbot, omgili, FacebookBot, cohere-ai, Timpibot | texto liberado, `/assets/fotos/` e `/assets/og/` bloqueados |

O bloqueio das fotos para treino é decisão de proteção: são 64 imagens com
crianças identificáveis e a autorização de uso de imagem segue pendente.
Conteúdo absorvido por base de treino não se retira depois. **Ao revisar essa
política, confirme antes se o termo de autorização foi assinado.**

Os bots de resposta continuam liberados, então o SECRI segue sendo encontrado e
citado pelas IAs — que é o que traz gente ao site.

---

## Estratégia de conteúdo

O site disputa **busca local**, não termo genérico. Uma ONG de bairro não vence
"projeto social" contra portal nacional, mas vence "ballet gratuito Vitória ES"
e "canoagem para adolescentes Vitória". Por isso:

- cidade e bairro aparecem no `title`, na `description` e no primeiro parágrafo
- cada projeto tem página própria, com uma intenção de busca só
- FAQ em toda página, que é o formato de resultado enriquecido e também o que
  as famílias realmente perguntam
- o primeiro parágrafo carrega a resposta, porque é dali que o Google extrai o
  trecho exibido

Ao escrever, não comece página com "fundado em 1988, o SECRI é uma entidade
civil filantrópica". Comece com o que a pessoa foi procurar.

---

## Estrutura e ferramentas

```
tools/
├── site.json            fonte única: nav, telefones, meta de cada página
├── partials/            head.html · header.html · footer.html
├── sync_chrome.py       escreve o chrome nas 20 páginas
├── gerar_projetos.py    gera projetos/*.html e projetos.html dos markdowns
├── gerar_seo.py         gera sitemap.xml e robots.txt
├── gerar_llms.py        gera llms.txt e llms-full.txt
├── trocar_main.py       troca o <main> de uma página
└── md.py                conversor Markdown→HTML mínimo
```

**Nunca edite header, footer ou `<head>` direto no HTML** — estão copiados em 20
arquivos e o `sync_chrome.py` sobrescreve. Includes por JavaScript não são
opção: `fetch()` é bloqueado em `file://` e o site abriria sem chrome.

**As páginas de projeto são geradas.** A fonte é
`../informacoes/conteudo/projetos/*.md`. Editar o HTML é perder o trabalho na
próxima geração.

Antes de encerrar qualquer alteração:

```bash
python3 tools/sync_chrome.py --check   # deve dar "0 divergentes"
```

---

## Esta versão é de validação

Informações não confirmadas aparecem **de propósito** com o selo `a confirmar`.
Cada página de projeto tem uma caixa listando o que falta, e `pendencias.html`
reúne tudo (não linkada, `noindex`).

Antes da publicação pública, nenhuma pode sobrar:

```bash
! grep -rq "a confirmar" *.html projetos/*.html || echo "há campos não confirmados"
```

---

## Pendências que bloqueiam a publicação

1. **Tailwind via Play CDN** compila no navegador e não é para produção. Gerar
   CSS compilado antes de publicar.
2. **Autorização de uso de imagem** das crianças nas fotos.
3. **Formulário de contato não envia nada** — há aviso visível na página. O de
   voluntariado aponta para o Google Form real e funciona.
4. **Depoimentos são ilustrativos.** As pessoas citadas não existem.
5. **Estatuto e atas** são digitalizações sem camada de texto; leitor de tela
   não lê. OCR resolveria.
6. **Domínio** assumido como `https://secri.org.br` em canonical, og:url e
   JSON-LD. Se mudar, é `base_url` no `site.json` e rodar a cadeia.
