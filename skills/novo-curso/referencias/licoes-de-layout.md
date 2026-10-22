# Lições de layout e roteiro

Checklist do que já foi apontado em revisões de clientes. Cada item diz o
erro que aconteceu e o que conferir. Use em dois momentos: **antes** do mapa
de seções (para ler o layout com estes olhos) e **antes de entregar**
(comparando cada captura com o layout).

Origem dos itens entre colchetes, para dar contexto: [EBANX 2026-10] =
curso EBANX LD/FT (`clientes/insight/ebanx/compliance`).

## Divisão em seções

- [ ] Cada bloco visual do layout virou uma seção, com fundo e espaçamento
  próprios — e não um slide inteiro numa seção só. [EBANX 2026-10: "flip
  cards e, abaixo, texto estático" estavam na mesma seção]
- [ ] Nenhuma seção foi criada só para esperar uma interação: o conteúdo do
  mesmo bloco que aparece depois (caixa de fechamento, texto de ponte) está
  na mesma seção com exibição condicional. [EBANX 2026-10: caixa logo abaixo
  de um componente virou outra seção]
- [ ] Não existe "buraco" (padding duplo) entre duas seções que no layout
  parecem uma só — se parecem uma, são uma. [EBANX 2026-10]
- [ ] Toda interação trava as seções seguintes **e** o conteúdo condicional
  da própria seção. [EBANX 2026-10: caixa abaixo do fluxo aparecia antes dos
  cliques]

## Forma: cantos, sombras, bordas

- [ ] Raio dos cantos medido no layout (normalmente pequeno); definido em
  token (`--radius-caixa`, `--radius-controle`), nunca no componente.
  [EBANX 2026-10: cantos grandes demais]
- [ ] Sombras: só onde o layout mostra. Cards, caixas, flip cards, fluxos e
  ícones em círculo geralmente **não** têm. Componentes genéricos que trazem
  sombra por padrão precisam da variável zerada no tema. [EBANX 2026-10]
- [ ] Bordas: ilustrações sem borda; player de vídeo pode ter (EBANX: borda
  branca). Conferir caso a caso.

## Cores

- [ ] Só a paleta do branding; tons "parecidos" do layout foram mapeados para
  o nome da paleta. [EBANX 2026-10: layout de IA com vários azuis]
- [ ] Cor de **texto** conferida no layout por elemento — títulos de cards,
  destaques dentro de caixas escuras, títulos de colunas. Não assumir "título
  = cor primária". [EBANX 2026-10: títulos de flip cards em preto + coral,
  não azul; destaques em azul dentro de caixas]
- [ ] Contraste AA: cor de destaque clara (coral, verde, pêssego) não é texto
  sobre branco; texto sobre fundo claro é o tom escuro da paleta.
- [ ] Ícone não some no fundo (ícone azul sobre círculo azul). [EBANX
  2026-10: ícone "cortado" era azul sobre azul]

## Composição e posição

- [ ] Ler o layout literalmente: lado da caixa de texto em relação à imagem,
  onde a faixa de cor de fundo termina (ex.: "um pouco depois do meio da
  imagem"), alinhamento do texto (esquerda × centro). [EBANX 2026-10: capa
  com caixa do lado errado e faixa até o fim da imagem]
- [ ] Ícone ao lado do título × acima dele; ícone dentro da caixa × em
  círculo fora dela. [EBANX 2026-10: ambos os casos]
- [ ] Seções com o mesmo desenho no layout usam o mesmo componente/variante
  (ex.: duas grades de cards iguais). [EBANX 2026-10]
- [ ] Colunas de título largas o bastante — título que quebra em muitas
  linhas quase sempre está numa coluna estreita demais. [EBANX 2026-10]
- [ ] Grupos de caixas lado a lado com a **mesma altura** e títulos ocupando
  a largura disponível. [EBANX 2026-10: fluxo]
- [ ] Texto de fechamento "solto" no layout (fonte maior, negrito) não é
  caixa. [EBANX 2026-10]
- [ ] Elementos decorativos (listras, faixas) nunca ficam sob o texto, em
  nenhuma largura. Medir no navegador: utilitários de padding
  podem perder para o padding do `.container`. [EBANX 2026-10]
- [ ] Aberturas com imagem sobre faixa de cor: conferir quanto a imagem passa
  da faixa (EBANX: vaza levemente; na capa, a faixa vai só até o meio).
  Medidas de posição feitas em JS devem usar `offsetTop/offsetHeight`, não
  `getBoundingClientRect`, que inclui o deslocamento das animações de
  entrada. [EBANX 2026-10]

## CSS

- [ ] Utilitários do template funcionam sem `!` (ex.: `mt-10` num `<p>`
  depois de outro `<p>`). Se precisar de `!`, alguma regra global está fora
  de `@layer`. [EBANX 2026-10: espaçamento entre textos ignorava os
  utilitários; container perdia a largura ao entrar em camada, porque o
  Tailwind v4 tem o próprio `container`]

## Texto (fidelidade ao roteiro)

- [ ] Todo texto veio do roteiro, não do layout (o layout de IA traz textos
  errados, resumidos ou repetidos).
- [ ] Hierarquia de títulos do roteiro preservada (h1/h2/h3 coerentes).
- [ ] Negrito, itálico e sublinhado exatamente como no roteiro — inclusive
  termos estrangeiros em itálico e links sublinhados.
- [ ] Maiúsculas/minúsculas como no roteiro, escritas no texto (sem
  `text-transform`). Caixa alta aplicada por estilo no pptx aparece como
  `[caps]` no extrator.
- [ ] Listas como listas (`<ul>/<ol>`), parágrafos como parágrafos.
- [ ] Instruções de produção do roteiro não aparecem na tela.

## Interações e estados

- [ ] Instrução de interação ("CLIQUE NOS ITENS…") no estilo do layout
  (EBANX: fundo translúcido, texto e borda brancos, canto leve).
- [ ] Linha do tempo/fluxo sequencial: itens ainda bloqueados ocultos (ou ao
  menos sem a linha), não "desabilitados" à mostra. [EBANX 2026-10]
- [ ] Questões (V/F, múltipla escolha): estado normal, hover, selecionado e
  gabarito claramente distintos; após confirmar, a escolha continua visível e
  o gabarito usa ícone (check/X) além da cor. [EBANX 2026-10]
- [ ] Botões que o layout não desenha (confirmar, avançar) são discretos e
  coerentes com o restante — não um botão grande e chamativo. [EBANX 2026-10]
- [ ] Vídeo/áudio: trava só após assistir/ouvir até o fim, se o roteiro pedir.
- [ ] Indicador de clique (mãozinha) visível por inteiro, sem ficar sob o
  item seguinte, em acordeões, flip cards e listas, no desktop e no celular.
  Itens com `position` + `z-index`, `transform` ou `perspective` criam
  contexto de empilhamento: o z-index precisa estar no item (ou no container
  dele) que tem o indicador. Conferir visualmente: a mão é um pseudo-elemento
  com `pointer-events: none`, então `elementFromPoint` não detecta o problema.
  [EBANX 2026-10]
- [ ] A última seção, se for curta, não tem animação de entrada
  (`v-entrada`; `data-aos` nos cursos antigos): no fim da página ela pode
  nunca alcançar o ponto de disparo e fica vazia. Testar rolando até o fim, sem desligar as animações. [EBANX
  2026-10]

## Tela a tela

- [ ] Cada tela cabe em 1280 × 720 sem corte (em dev, o console avisa qual
  tela passa da altura).
- [ ] Sem `sm:`/`md:`/`lg:` nem `vh` dentro das telas: o canvas é fixo e
  escalado, eles leem a janela.
- [ ] Telas com interação: o "avançar" fica bloqueado até concluir, e a
  dica aparece; telas sem interação liberam após o tempo de leitura.

## Responsividade e acessibilidade

- [ ] (rolagem) 390px: sem rolagem horizontal; ícones e títulos lado a lado não
  espremem o texto (reduzir o ícone no celular).
- [ ] Foco visível em todos os controles; interações por teclado.
- [ ] Ilustração com personagem tem `alt` descritivo; decorativa `alt=""`.
- [ ] Conteúdo que aparece após interação anunciado (`aria-live`).
