# Formatos de arquivo de ajustes

Modelos de arquivo de ajustes já recebidos e como interpretá-los. Ao receber
um arquivo num formato que não está aqui, interprete-o pelas regras gerais do
`SKILL.md` e, no fim, **acrescente uma seção nova** descrevendo o modelo
(como identificar, onde estão o "antes" e o "depois", armadilhas), com um
exemplo real.

---

## Modelo A — prints anotados com caixas amarelas

Origem: Claro — Trilha de Melhoria Contínua (`clientes/claro/trilha-da-qualidade/multipage/tmp/ajustes.pptx`, ajustes do módulo 2, out/2026).

### Como identificar

- Cada slide é **um print de tela do curso** (ocupando quase todo o slide)
  com **caixas amarelas** por cima.
- Cada caixa começa com um **verbo em negrito**: `SUBSTITUIR`, `INCLUIR`,
  `EXCLUIR` — às vezes com complemento (`SUBSTITUIR imagem e título`,
  `SUBSTITUIR os feeds do Medidor`, `INCLUIR como no 1º módulo o botão da
  Receita`).
- Uma **linha tracejada** liga a caixa a um **retângulo tracejado** no
  print, que marca o alvo.
- O arquivo não diz módulo nem seção: descubra pelo print (banner do
  módulo, títulos) e por `grep` no `pt-BR.json`. Os slides seguem a ordem
  do curso.

### Onde está o "antes" e o "depois"

- **Antes**: o trecho dentro do retângulo tracejado, **visível só no
  print** — o extrator não o captura. Leia-o no PDF renderizado e ache a
  chave com `grep` de um pedaço distintivo da frase.
- **Depois**: o texto da caixa amarela (vem no relatório do extrator, com
  negrito marcado).
- Os retângulos tracejados não têm texto; associe caixa ↔ alvo pela linha
  tracejada no visual.

### Regras por verbo

| Caixa | Alvo | Significa | Tipo |
| ----- | ---- | --------- | ---- |
| `SUBSTITUIR` + texto | trecho de texto | troca **só o trecho marcado** | simples |
| `SUBSTITUIR` + texto curto | palavra no meio da frase | troca a palavra (ex.: "Ação" → "Aperfeiçoamento") | simples |
| `SUBSTITUIR` + texto | parágrafo(s) inteiro(s) | troca o bloco todo | simples |
| `SUBSTITUIR imagem…` | imagem/ícone | troca de asset — ver regras de asset | simples se o asset vier entregue; senão ❓ |
| `EXCLUIR` | trecho de texto | apaga o trecho e acerta espaços/pontuação | simples |
| `EXCLUIR` | seção/bloco inteiro | remove bloco ou seção | estrutural |
| `INCLUIR` + texto | área vazia entre blocos | conteúdo novo (bloco ou seção nova) | estrutural |
| `INCLUIR` imagem | espaço vazio dentro de um bloco | muda o layout + imagem (placeholder) | estrutural |
| `INCLUIR como no módulo N…` | — | reaproveitar o padrão daquele módulo (ache-o e copie) | estrutural (plano curto) |
| qualquer | print de um PDF (caderno) | o ajuste é no **arquivo PDF**, não no código | ❓ pendente: PDF novo a ser entregue |

### Armadilhas observadas

- **Âncoras no texto novo**: a caixa costuma repetir palavras vizinhas do
  trecho marcado para situar a troca. Ex.: alvo "raiz." em "Definir ações
  após identificar a causa raiz." e caixa "raiz, prazo 01/01 a 15/01." →
  resultado "Definir ações após identificar a causa raiz, prazo 01/01 a
  15/01."; alvo "FCA." e caixa "**FCA** (Fato, Causa, Ação). Por" → o "Por"
  é só a âncora da frase seguinte. Alinhe início e fim do texto novo com a
  frase original para não duplicar nem perder palavras.
- **Negrito da caixa** vira `<strong>` no trecho trocado; fora dele, mantenha
  o HTML que já existe.
- **Deslizes de digitação na caixa** (espaço antes de dois-pontos, como
  "PARA QUE SERVE :", espaço duplo): normalize e cite no resumo.
- **Mesma troca em vários slides** (ex.: "PARA O QUE SERVE" → "PARA QUE
  SERVE" em cada item do acordeão, um por slide): aplique em cada alvo
  marcado. Ocorrências do mesmo termo **não marcadas** (outras seções ou
  módulos): **não altere**, liste como ⚠️ para o cliente decidir.
- **Imagens dentro das caixas** são referências (muitas vezes prints de
  e-mail, recortados e em baixa resolução): **nunca** viram asset. Se a
  imagem de referência tiver **legenda embutida** (texto realçado no
  próprio print), esse texto provavelmente é copy para o curso —
  transcreva-o e inclua no planejamento como texto a confirmar.
- **Prints pequenos de contexto** (ex.: miniatura no canto mostrando de
  onde se abriu um modal) só situam o ajuste; não são referência de asset.
- **Menções a e-mail/pessoa/data** ("imagem que o cliente printou no
  e-mail … dia 01/10") são rastreabilidade: cite no resumo, não no curso.
- **Link externo** numa caixa (ex.: URL de receita) é o `href` do botão a
  criar/alterar.
