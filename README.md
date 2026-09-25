# ong-secri

Site do **SECRI — Serviço de Engajamento Comunitário**, Vitória/ES.

HTML estático puro, sem build. Abra `index.html` direto no navegador.

## Esta versão é de validação

O site está com o conteúdo real do SECRI, mas **informações ainda não confirmadas aparecem de propósito**, marcadas com o selo `a confirmar` em âmbar. Cada página de projeto traz no topo uma caixa listando o que falta validar.

`pendencias.html` reúne tudo em uma página só. Não está no menu nem no sitemap, e serve de roteiro para a reunião de validação com o cliente.

**Antes de publicar de verdade**, nenhum `a confirmar` pode sobrar:

```bash
! grep -rq "a confirmar" *.html projetos/*.html || echo "Ainda há campos não confirmados"
```

## Estrutura

```
├── index.html  quem-somos.html  projetos.html  impacto.html
├── noticias.html  transparencia.html  como-ajudar.html  contato.html
├── politica-privacidade.html  404.html
├── pendencias.html          ← interna, noindex, fora do menu
├── projetos/                ← 8 páginas, uma por projeto
├── assets/
│   ├── fotos/<projeto>/     ← 64 WebP, máx. 1600px, todos < 300 KB
│   ├── parceiros/           ← logos padronizados em 600x240 transparente
│   ├── documentos/          ← 11 PDFs de transparência
│   └── theme.js site.js     ← tokens do Tailwind e comportamento
└── tools/                   ← manutenção, não é build
```

## Editar o cabeçalho, o rodapé ou o `<head>`

**Não edite direto no HTML** — eles estão copiados em 19 arquivos e serão sobrescritos.

A fonte única é `tools/`:

| Arquivo | O que controla |
|---|---|
| `tools/site.json` | navegação, telefones, título e descrição de cada página, `og_image`, `noindex` |
| `tools/partials/head.html` | `<head>`, meta tags, favicons |
| `tools/partials/header.html` | cabeçalho e menu |
| `tools/partials/footer.html` | rodapé |

Depois de editar:

```bash
python3 tools/sync_chrome.py --check    # mostra o que mudaria
python3 tools/sync_chrome.py --apply    # aplica nas 19 páginas
```

O script só reescreve as regiões de chrome. O corpo de cada página, entre `<main>` e `</main>`, nunca é tocado.

Includes por JavaScript foram descartados de propósito: `fetch()` é bloqueado em `file://`, e o site precisa abrir com dois cliques.

## Editar o conteúdo dos projetos

As 8 páginas de projeto e a listagem são **geradas** a partir dos markdowns em `../informacoes/conteudo/projetos/`. Editar o HTML direto é perder o trabalho na próxima geração.

```bash
python3 tools/gerar_projetos.py     # regenera projetos/ e projetos.html
python3 tools/sync_chrome.py --apply
```

O gerador ignora as seções "Fotos", "Depoimento" e "Dados estruturados" dos markdowns — são notas de produção. O JSON-LD é extraído da última e injetado na página.

A galeria de cada projeto e a cor de cada eixo ficam no topo de `tools/gerar_projetos.py`.

## Paleta

`assets/theme.js` define `rose`, `sky`, `gold`, `verde`, `laranja` e os neutros `ink`. Cores por **eixo temático**, não por projeto:

| Eixo | Cor |
|---|---|
| Arte e cultura | `rose` |
| Educação e aprendizagem | `sky` |
| Esporte e inclusão | `verde` |
| Convivência e bem-estar | `laranja` |

`gold` é reservado para doação e para o selo `a confirmar`. Usá-lo como cor de projeto faz o botão de doar perder destaque.

Todos os degraus `700` passam em contraste AA sobre branco. Ao criar uma cor nova, verifique antes.

## Pontos de atenção antes de publicar

1. **Tailwind via Play CDN.** Compila no navegador, avisa no console e não é para produção. Antes de ir ao ar, gerar um CSS compilado.
2. **Autorização de imagem** das crianças nas fotos — pendente, e é bloqueante.
3. ~~Formulário de contato não envia nada.~~ Resolvido: abre o WhatsApp (27) 99849-9507 com a mensagem pronta (Web no PC, app no celular). O de voluntariado aponta para o Google Form real e funciona.
4. **PDFs comprimidos** de 71 MB para 25 MB. Os originais estão em `../informacoes/transparencia/`. Quando forem para um bucket, basta trocar o caminho `assets/documentos/`.
5. **Estatuto e atas não têm camada de texto** — são digitalizações. Leitor de tela não lê. OCR resolveria.
6. **Depoimentos são ilustrativos.** As pessoas citadas não existem; há selo avisando. Substituir por falas reais antes da publicação.
