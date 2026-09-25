# Análise de conformidade — requisitos de transparência

**Site:** SECRI - Serviço de Engajamento Comunitário (versão de validação)
**Data da análise:** 24/09/2026
**Escopo:** verificar se o site atende aos 9 requisitos de transparência exigidos
para a organização, apontando o que já existe e o que falta.

---

## Resumo

Os 9 requisitos têm alguma presença no site. Nenhum está totalmente ausente,
mas **três não passariam numa checagem rigorosa**:

- ~~**Diretoria e Conselho** — os nomes não estão publicados~~ (resolvido em 25/09/2026)
- **Demonstrações contábeis** — só Balanço e DRE, sem notas explicativas
- **Página de doação** — existe, mas misturada com voluntariado e empresas

| # | Requisito | Situação | Onde está |
|---|---|---|---|
| 1 | Site institucional | ✅ Atende | Site completo |
| 2 | Página de doação | ⚠️ Parcial | `como-ajudar.html` |
| 3 | Missão da organização | ✅ Atende, sem link direto | `quem-somos.html`, seção "Missão, Visão e Valores" |
| 4 | Projetos e ações | ✅ Atende | `projetos.html` + 8 páginas em `projetos/` |
| 5 | Estatuto Social | ✅ Atende | `transparencia.html` e rodapé |
| 6 | Diretoria e Conselho | ✅ Atende (25/09/2026) | `quem-somos.html#diretoria` e rodapé |
| 7 | Relatório anual (ano anterior) | ✅ Atende | Relatórios 2025, 2024 e 2023 |
| 8 | Demonstrações contábeis (ano anterior) | ⚠️ Parcial | `balanco-dre-2025.pdf` |
| 9 | Página de contato | ✅ Atende, com pendências | `contato.html` |

---

## Detalhamento por requisito

### 1. Site institucional — ✅ Atende

Site com 17 páginas públicas, menu com Início, Quem Somos, Projetos, Impacto,
Notícias, Transparência e Contato. SEO, dados estruturados e sitemap
configurados.

### 2. Página de doação — ⚠️ Parcial

**O que já tem** (`como-ajudar.html`):

- Pix com chave CNPJ 31.795.321/0001-53 e titular
- Transferência bancária: SICOOB (756), agência 3010, conta 56729-9
- Nota Premiada Capixaba, com passo a passo
- Doação de materiais, com lista de itens e endereço de entrega
- Canal para empresas (setor financeiro)
- Origem dos recursos da instituição
- Botão "Doar" no cabeçalho e no rodapé

**O que falta:**

- **Página específica.** A página se chama "Como Ajudar" e mistura doação,
  voluntariado e empresas. Um avaliador literal pode não reconhecê-la como
  "página de doação". Não há URL própria (ex.: `doe.html`).
- **Destino do dinheiro.** Nada diz em que a doação é aplicada, nem exemplos
  do tipo "R$ 50 = um mês de material de oficina".
- **Recibo/comprovante.** Não explica como o doador pede recibo.
- **QR Code do Pix** e botão de copiar a chave.
- **Benefício fiscal.** Não informa se a doação é dedutível, o que depende do
  CEBAS, hoje marcado "a confirmar".

### 3. Missão da organização — ✅ Atende, sem link direto

**O que já tem:** missão, visão, propósito, valores e objetivos em
`quem-somos.html`.

**O que falta:** o requisito pede "um link que direcione" à missão. Hoje ela
fica no meio da página, sem âncora, e nenhum link aponta para ela.

**Sugestão:** âncora `quem-somos.html#missao` e link "Missão e Valores" no
rodapé, bloco Institucional.

### 4. Projetos e ações — ✅ Atende

`projetos.html` no menu principal, com os 8 projetos ativos, cada um com página
própria (público, horários, local, FAQ). A página inicial destaca 4 deles.

Observação: as páginas de projeto ainda têm campos "a confirmar", que precisam
ser resolvidos antes da publicação.

### 5. Estatuto Social — ✅ Atende

`assets/documentos/estatuto-social.pdf` (36 páginas, 8,5 MB), em
`transparencia.html#estatuto` e no rodapé de todas as páginas.

**Ressalva:** o PDF é digitalização sem camada de texto. Não é pesquisável e
leitor de tela não lê. Um OCR resolveria e reduziria o tamanho do arquivo.

### 6. Diretoria e Conselho — ✅ Atende (resolvido em 25/09/2026)

> Nomes publicados em `quem-somos.html#diretoria`, com link no rodapé e em
> Transparência. O texto abaixo registra a situação encontrada na análise.

**Situação atual:** `quem-somos.html` mostra só a estrutura organizacional
(Conselho Fiscal, Diretoria Executiva, Coordenação etc.) e diz:
"Composição nominal da Diretoria e do Conselho Fiscal: a confirmar".

Os nomes existem apenas dentro de `ata-eleicao-e-posse-2026-2028.pdf`, que é
imagem escaneada. O avaliador dificilmente vai procurar ali, e leitor de tela
não lê.

**O que falta:** lista publicada no site com nome e cargo de:

- Diretoria Executiva
- Conselho Fiscal
- Conselho Deliberativo/Consultivo, se houver
- Mandato vigente (2026-2028)

**Dependência:** autorização da equipe para divulgar os nomes, como o próprio
texto do site já registra.

### 7. Relatório(s) anual(is) — ✅ Atende

Relatórios de Atividades 2025 (43 p.), 2024 (21 p.) e 2023 (17 p.) em
`transparencia.html`. O mais recente é de 2025, ano anterior ao atual, como
exige o requisito.

### 8. Demonstrações contábeis e financeiras — ⚠️ Parcial

**O que já tem:** `balanco-dre-2025.pdf` com 2 páginas, Balanço Patrimonial em
31/12/2025 (comparativo com 2024) e DRE, assinados pela presidente e pelo
contador (CRC-ES 011119-O), com assinatura digital de 17/08/2026. Atende ao
critério de ano anterior.

**O que falta:**

- **Notas explicativas.** O arquivo original se chamava "NE 2025", o que sugere
  que existem e ficaram de fora do PDF publicado.
- **Demonstração dos Fluxos de Caixa (DFC)** e **Demonstração das Mutações do
  Patrimônio Líquido (DMPL)**, que compõem o conjunto completo exigido para
  entidades sem fins lucrativos (ITG 2002 (R1)).
- **Parecer do Conselho Fiscal** aprovando as contas.
- **Histórico.** Só há 2025. Publicar 2024 e 2023 deixaria a série igual à dos
  relatórios.
- **Organização da página.** As demonstrações estão misturadas com os
  relatórios em "Prestação de contas". Uma seção própria, "Demonstrações
  contábeis", facilita a checagem.

### 9. Página de contato — ✅ Atende, com pendências

**O que já tem** (`contato.html`): endereço completo com CEP, WhatsApp, telefone
fixo, e-mail geral, e-mail financeiro e Instagram.

**Pendências antes da publicação:**

- Formulário não envia nada (há aviso visível)
- Horário de atendimento "a confirmar"
- Mapa é um marcador de posição, sem o Google Maps
- Link do YouTube "a confirmar"

Para o requisito, os dados atuais bastam. Para publicar, as pendências precisam
sair.

---

## Outros pontos de atenção

- **Selo "CEBAS a confirmar"** em Transparência e Quem Somos. Se a entidade
  não tem CEBAS, remover o selo é melhor que deixá-lo pendente, porque passa
  impressão de irregularidade.
- **Documentos sem texto.** Estatuto e ata de eleição são imagens pesadas
  (8,5 MB e 4,6 MB). OCR os tornaria pesquisáveis e acessíveis.
- **Depoimentos fictícios.** As pessoas citadas não existem. Numa avaliação de
  transparência isso é risco reputacional; trocar por depoimentos reais ou
  remover antes de publicar.

---

## Plano de ação

| Prioridade | Ação | Requisito | Depende de |
|---|---|---|---|
| 1 | ✅ Publicar nomes e cargos da Diretoria e do Conselho — **feito** | 6 | Organização: lista e autorização |
| 2 | Completar demonstrações 2025 (notas, DFC, DMPL, parecer) e publicar 2024 | 8 | Organização: contador |
| 3 | ✅ Âncora e link direto para a Missão — **feito** | 3 | Só desenvolvimento |
| 4 | ✅ Página de doação própria (`doe.html`), QR Code, recibo, destino do recurso — **feito**, com dados "a confirmar" | 2 | Desenvolvimento + dados da organização |
| 5 | Seção separada para demonstrações contábeis em Transparência | 8 | Só desenvolvimento |
| 6 | Formulário, horário, mapa e YouTube no Contato | 9 | Organização: destino do formulário, horário, links |
| 7 | Resolver selo CEBAS | — | Organização |
| 8 | OCR em estatuto e atas | 5, 6 | Só desenvolvimento |
| 9 | Trocar ou remover depoimentos fictícios | — | Organização |

---

## Andamento (24/09/2026)

- **Missão:** `quem-somos.html#missao` criada; link "Missão e Valores" no rodapé
  de todas as páginas.
- **Doação:** nova página `doe.html` com Pix (QR Code, chave e copia e cola
  com botão Copiar), transferência, Nota Premiada, destino do recurso, recibo,
  dedução fiscal, doação de materiais e FAQ com `FAQPage`. Botão do cabeçalho
  virou "Doe agora". `como-ajudar.html` ficou com voluntariado e empresas.
  Pendentes: exemplos de valores, prazo do recibo, dedutibilidade. O QR Code
  precisa ser testado num app de banco antes de publicar.
- **Diretoria e Conselho (25/09/2026):** seção `quem-somos.html#diretoria` com
  Diretoria Executiva (4 cargos) e Conselho Fiscal (3 membros), gestão
  2026-2028, link para a ata. Link "Diretoria e Conselho" no rodapé e chamada
  em Transparência.
- **CEBAS:** mantido como está, aguardando confirmação.
