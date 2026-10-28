---
name: ajustes-curso
description: Aplica ajustes pedidos pelo cliente ou pela revisão em cursos e-learning da Plural (feitos da plural-curso-base ou anteriores a ela: Vue + SCORM com `secoes.ts`, `store.ts`, `pt-BR.json`) — correções de texto, troca de assets (imagens, vídeos, áudios, PDFs), mudanças de layout e adição/remoção/reordenação de seções. Use quando receber um arquivo de ajustes (geralmente .pptx), uma lista de ajustes, um apontamento de revisão ("no slide X trocar…", "corrigir texto da seção…", "tirar a seção…", "incluir uma tela…") ou um asset novo para substituir.
argument-hint: "[arquivo-de-ajustes.pptx]"
---

# Ajustes no curso

Você é a pessoa responsável por aplicar os ajustes no curso. Recebe
apontamentos (do cliente, da revisão de texto, do design) e os transforma em
mudanças no código, sem quebrar o progresso do aluno, a trava das seções nem o
build SCORM.

Arquivo/pedido recebido: $ARGUMENTS

Se veio um caminho acima, é o arquivo de ajustes a processar. Se veio vazio,
use o arquivo ou o pedido mencionado na conversa; sem nenhum dos dois,
pergunte qual é o arquivo de ajustes.

Arquivos de apoio desta skill (em `~/.claude/skills/ajustes-curso/`):

- `formatos-de-ajuste.md` — modelos de arquivo de ajustes já vistos e como
  interpretá-los (compartilhado entre todos os projetos/clientes).
- `scripts/extrair-pptx.py` — extrator de .pptx.

## 0. Conhecer o projeto

Esta skill serve a vários cursos Plural. Antes de mexer:

1. Leia o `CLAUDE.md` (e o `README.md`) do curso. **O que estiver lá
   prevalece sobre este roteiro** — componentes próprios, regras de
   espaçamento, convenções de chaves.
2. Veja se o curso foi **feito da `plural-curso-base`** (seção "Origin" do
   `CLAUDE.md`, `src/plural/versao.ts`, `src/config/definicao-curso.ts`).
   A maioria dos passos abaixo segue essa estrutura:
   - `src/config/definicao-curso.ts` — rolagem ou tela a tela, menu,
     travas, conclusão; `versao` (mudar zera o progresso em dev). Leia por
     `definicaoCurso()`; referência em `DEFINICAO-CURSO.md`.
   - `src/config/secoes.ts` — `montarSecoes("m01", [[Componente,
     concluida, opções], …])`: ids (`m01s1`…) e desbloqueio sequencial
     gerados pela posição; `menu: { titulo }` marca item do menu.
   - `src/config/store.ts` — schema Zod do `suspendData`.
   - `src/config/modulos.ts`, `modulos-ids.ts` — módulos.
   - `src/assets/locales/pt-BR.json` — textos (`m01-s02-…`).
   - `src/views/modulo-N/secao-M.vue` — uma seção por arquivo.
   - `src/components/` — wrappers `App*` e componentes do curso.
   - `src/plural/` e `src/core/` — **não editar** (vêm da base). Se faltar
     algo genérico, resolva no curso e registre a lacuna para a base
     (skill `componente-plural`).
   - `docs/guia-conteudo.md` (seção e módulo novos) e
     `docs/guia-wrapper-app.md`; o `?catalogo` em dev mostra cada
     componente com props, variáveis e schema do `suspendData`.
3. **Curso anterior à base** (sem `definicao-curso.ts`/`montarSecoes`,
   com `app-definition.ts`, AOS, tuplas `mNNConcluidas`): aplique as mesmas
   etapas — ler, mapear, classificar, aplicar, verificar, retornar — com os
   caminhos e padrões que o curso usa; as notas "curso antigo" abaixo
   ajudam.
4. Veja os scripts do `package.json` (typecheck, lint, lint:css, build,
   build:validacao) — serão usados na verificação.

## 1. Ler o arquivo de ajustes (.pptx)

Os ajustes geralmente chegam num `.pptx`. **Leia
`~/.claude/skills/ajustes-curso/formatos-de-ajuste.md`** e identifique qual
modelo de arquivo é este — cada modelo tem suas convenções (onde fica o
texto antigo, o que cada marcação significa, armadilhas já vistas).

Leia o arquivo de duas formas; nenhuma basta sozinha:

1. **Relatório do extrator** — caixas de texto por slide (com negrito
   `**x**`, itálico `*x*`, sublinhado `<u>x</u>`, riscado `~~x~~`, realce
   `==x==`; caixa alta de estilo já em maiúsculas), imagens classificadas
   (`print da tela` × `referência`, e em qual caixa a referência está),
   notas e comentários:

   ```sh
   python3 ~/.claude/skills/ajustes-curso/scripts/extrair-pptx.py arquivo.pptx <scratchpad>/ajustes > <scratchpad>/ajustes.md
   ```

   As imagens vão para `<scratchpad>/ajustes/` já recortadas como no slide,
   **só para consulta**. (Usa Pillow para recortar, se instalado.)
2. **Visual** — converta para PDF e leia as páginas (Read com `pages`, até
   20 por vez). É aqui que se vê o alvo de cada caixa (retângulos, setas,
   linhas tracejadas) e o texto **antigo** no print:

   ```sh
   soffice --headless --convert-to pdf --outdir <scratchpad> arquivo.pptx
   ```

Se o arquivo não se encaixar em nenhum modelo conhecido, interprete-o pelas
regras deste roteiro e, ao terminar, documente o novo modelo em
`formatos-de-ajuste.md` (como identificar, antes/depois, armadilhas,
exemplo e projeto de origem).

Ignore o que não é ajuste: instruções de produção ("PRODUÇÃO:",
"VALIDADORAS:"), sugestões de ícone/BG e menções a e-mails/pessoas/datas
(estas vão só para o resumo, como rastreabilidade).

## 2. Mapear e classificar

Monte uma tabela com **um item por caixa/marcação**, numerado
`S<slide>.<caixa>` (ex.: `S9.2`):

| Item | Ação | Seção (`mNNsMM`) | Chave/arquivo | Antes → depois | Tipo |
| ---- | ---- | ---------------- | ------------- | -------------- | ---- |

Para localizar (ver seção 3): ache o texto **antigo** visto no print com
`grep` no `pt-BR.json` e, pela chave, a seção.

Classifique cada item:

| Tipo | Exemplos | Ação |
| ---- | -------- | ---- |
| **Simples** | trocar/corrigir/excluir trecho de texto, feedbacks, títulos, menu, dicas; trocar asset **por arquivo entregue** equivalente; alt text | **aplicar direto**, sem pedir confirmação |
| **Estrutural** | incluir bloco/texto novo numa área vazia, incluir imagem onde não havia, botão/componente novo (inclusive "como no módulo N"), trocar tipo de interação ou layout, adicionar/remover/reordenar seções, nova conquista, qualquer mudança no `store.ts` | **mostrar o planejamento e esperar aprovação** |
| **Pendente** | troca de imagem sem asset entregue, ajuste dentro de PDF, alvo ou texto ambíguo | não aplicar; listar a pergunta ou o que falta |

Na dúvida entre simples e estrutural, trate como estrutural.

Fluxo:

1. Aplique todos os itens **simples** (seções 4 e 5) e rode a
   verificação (seção 8).
2. Se houver itens **estruturais**, apresente o planejamento e **pare**
   até a aprovação. Para cada item:
   - slide do ajuste → seção afetada (`mNNsMM`, arquivo)
   - o que muda e qual modelo/componente (do catálogo ou de outro módulo)
     será usado
   - textos novos que entram (incluindo legendas transcritas de imagens
     de referência, marcadas como "a confirmar")
   - onde entra placeholder de imagem
   - arquivos que serão tocados
   - impacto no progresso do aluno (`suspendData`), se houver — ver
     seção 7
   - dúvidas em aberto
3. Após a aprovação, aplique os estruturais e rode a verificação de novo.

Itens pendentes não bloqueiam os demais.

## 3. Localizar cada ajuste

- Por texto (o caso mais comum): pegue um trecho distintivo do texto
  **antigo** (5–8 palavras, sem pontuação/HTML nas pontas, pois o JSON tem
  `<strong>` no meio das frases) e faça
  `grep -n "trecho" src/assets/locales/pt-BR.json`; depois
  `grep -rn "chave" src/` para achar a seção. Se não achar, encurte o
  trecho — o print pode ter quebras ou pequenas diferenças.
- Nem todo curso guarda os textos no `pt-BR.json` (ex.: simuladores com
  HTML em template strings em `src/composables/*-data.ts`). Se não houver
  locale ou o `grep` nele não achar nada, faça `grep -rn` em `src/`.
- Por número: "módulo 2, seção 5" → `src/views/modulo-2/secao-5.vue`,
  id `m02s5`, chaves `m02-s05-*` (confira o padrão de chaves do projeto).
- Por imagem: identifique o asset na seção já localizada (imports no
  `.vue`) e confira abrindo o arquivo.
- A numeração dos slides do arquivo de ajustes **não** é a das seções.
  Roteiros e layouts originais costumam ficar em `tmp/` (fora do git),
  úteis para contexto.
- O arquivo pode não dizer o módulo: deduza pelo print (banner, títulos) e
  confirme pelo `grep`.
- Ao trocar um termo (nome de programa, rótulo), faça `grep` do termo
  antigo no curso inteiro: ocorrências **não marcadas** no arquivo de
  ajustes não são alteradas — liste-as como ⚠️ no resumo.

## 4. Correção de texto

Todo texto do curso fica em `src/assets/locales/pt-BR.json` (ou nos outros
locales que o projeto tiver — ajuste todos os que existirem).

- Edite **o valor** da chave; não renomeie chaves.
- Troque **só o trecho marcado**. O texto novo costuma trazer palavras
  vizinhas como âncora: alinhe início e fim com a frase original para não
  duplicar nem perder palavras, e acerte espaços e pontuação nas emendas
  (exemplos em `formatos-de-ajuste.md`).
- Preserve o HTML existente (`<strong>`, `<br>`, `<em>`, listas) a menos que
  o ajuste peça para mudar a formatação. Negrito/itálico pedido no
  apontamento vira `<strong>`/`<em>` — a chave precisa ser renderizada com
  `v-html` (confira no `.vue`; se for `{{ $t(...) }}`, troque para
  `v-html`).
- Antes de editar, verifique se a chave é reaproveitada em outro lugar
  (`grep -rn "chave" src/`). Se for, e o ajuste valer só para um ponto,
  crie uma chave nova para esse ponto.
- Textos fixos no `.vue` (fora do JSON) são exceção: mova-os para o JSON
  seguindo o padrão de chaves do projeto.
- Lembre dos textos fora das seções: títulos do menu de seções
  (`menu: { titulo }` em `secoes.ts`; curso antigo: `menuTitle`), dicas/popovers definidos em `secoes.ts`, títulos de
  conquistas, alt texts.
- Mantenha aspas tipográficas, travessões e acentuação do texto recebido.
  Não "melhore" o texto além do que foi pedido; se notar outro erro,
  aponte no resumo em vez de corrigir por conta.

## 5. Assets

**Imagens e mídias que vêm dentro do .pptx nunca viram asset do curso** —
são prints, recortes de e-mail e referências de baixa qualidade. Assets
reais só entram quando entregues como arquivo separado (ex.:
`tmp/.../novos-assets/`), enviados ou indicados por quem pediu os ajustes.

Assets costumam ficar em `src/assets/{img,video,audio,anexos}/` e entram
por `import` no `.vue`/`.ts`.

### Com o arquivo entregue

Os assets podem chegar **soltos ao lado do arquivo de ajustes** (ex.: em
`tmp/`, com o mesmo horário de modificação), já com o **mesmo nome** do
arquivo em `src/assets/` — nesse caso é sobrescrita. Confira se o asset
alvo de cada slide é mesmo o que veio: uma imagem composta (personagem
sobre fundo) pode não ter vindo, mesmo que a versão recortada do
personagem tenha. Arquivos entregues com o mesmo nome de um asset do curso
mas não marcados em nenhum slide podem ser aplicados, com ⚠️.

1. Ache onde o asset atual é usado: `grep -rn "nome-do-arquivo" src/`.
2. Olhe o asset atual e o novo (Read na imagem) para confirmar que é a troca
   certa e se a proporção mudou — se mudou a ponto de exigir rearranjo,
   vira item estrutural.
3. **Mesmo formato e mesmo papel** → sobrescreva o arquivo mantendo o nome
   (nenhum import muda). **Formato ou nome diferente** → copie o novo
   arquivo, atualize o import e apague o antigo se não houver mais
   referências.
4. Atualize o `alt` no `pt-BR.json` se o conteúdo da imagem mudou.
5. O build SCORM costuma embutir tudo num único `index.html`: confira o
   tamanho (`ls -lh`). Arquivos de vários MB ou com resolução muito maior
   que a exibida devem ser sinalizados — sugira otimizar antes de incluir.

### Sem o arquivo entregue

- **Troca** de imagem existente: mantenha a imagem atual e marque o item
  como ❓ pendente — "aguardando asset" — com a descrição do que foi pedido
  (e da referência, se houver).
- **Inclusão** de imagem onde não havia: use um placeholder e um `alt` que
  descreva a imagem pretendida (com base na referência), e marque ⚠️
  "placeholder — aguardando asset".
  - Procure placeholders já existentes no projeto
    (`find src -iname "*placeholder*"`) e use o mesmo padrão de nome/local.
  - Sem placeholder de imagem, crie `src/assets/img/placeholder.png`:

    ```sh
    magick -size 1600x900 xc:'#d9d9d9' -gravity center -pointsize 64 -fill '#222222' -annotate 0 'IMAGEM PENDENTE' src/assets/img/placeholder.png
    ```

  - Verifique se o `.gitignore` ignora placeholders
    (`git check-ignore -v <arquivo>`). Se ignorar, o build num clone limpo
    falha enquanto algum estiver em uso — o que impede publicar com
    placeholder. Informe no resumo em qualquer caso.

### Anexos e PDFs

- **Anexo novo a linkar**: copie o arquivo para `src/assets/anexos/` (ou
  onde o projeto guardar anexos) e siga o padrão de link já existente. Se
  ele chegar em formato diferente do citado no ajuste (ex.: pedido
  `.docx`, entregue `.pdf` com o mesmo nome), confirme qual usar.
- **Ajuste no conteúdo de um PDF** (caderno, anexo) = PDF novo a ser
  entregue pelo design; não há o que mudar no código até lá. Antes de
  marcar ❓, veja se o PDF novo já veio junto com o arquivo de ajustes
  (confira com `pdftotext` se ele já traz o texto pedido) — se veio, é
  troca de asset.

## 6. Mudança de layout

1. Procure o layout pedido no `?catalogo` e em seções parecidas do próprio
   curso (`grep` por componentes). Use os blocos `PluralLayout*` e os
   componentes da `plural/` e de `src/components/`; não escreva layout com
   classes soltas quando houver bloco pronto.
2. Identidade só por variáveis CSS (no wrapper `App*` ou na seção) e
   tokens do tema (`bg-primary`, `rounded-caixa`…); nada de cor solta nem
   `:deep()` em `components/` (o lint barra).
3. Rolagem: confira celular (390) e desktop. **Tela a tela**: cada tela
   cabe em 1280 × 720, sem `sm:`/`md:`/`lg:` nem unidades de viewport
   (o layout quebra por `@container`); exercícios apertados →
   `plural-exercicio-compacto`.
4. Animações de entrada pelo `v-entrada` (curso antigo: `data-aos`),
   coerentes com as seções vizinhas.
5. Botões que navegam (ir para o exercício, começar):
   `useNavegacaoCurso()` (`avancar()`, `irParaSecao("m01s4")`).
6. Se o ajuste trocar o **tipo de interação** de uma seção (ex.: abas →
   flip cards, ou estática → interativa), trate também a persistência como
   na seção 7 (schema em `store.ts`, conclusão em `secoes.ts`,
   `exibeTrava`).
7. Componente novo: genérico → base (skill `componente-plural`), contornando
   no curso enquanto isso; só do curso → `src/components/`.

## 7. Adicionar, remover ou reordenar seções

Cada seção mexe em vários lugares ao mesmo tempo (passo a passo no
`docs/guia-conteudo.md` do curso):

| Onde | O quê |
| ---- | ----- |
| `src/views/modulo-N/secao-M.vue` | o conteúdo |
| `src/config/secoes.ts` | import e entrada `[Componente, concluida, opções]` na posição certa da lista do `montarSecoes` (o id e o desbloqueio vêm da posição); `menu: { titulo }` se iniciar item do menu |
| `src/config/store.ts` | chave da seção no schema e no padrão (só seções interativas) |
| `src/assets/locales/pt-BR.json` | chaves da seção |
| `irParaSecao("mNNsM")` e links | ids citados em outras seções |
| `README.md` | mapa das seções |

Curso antigo: entrada com `id`/`menuTitle` e lógica de `desbloqueada`/
`concluida` (tupla `mNNConcluidas` + `acumulaDesbloqueio`: posição, tipo da
tupla e índices); conquistas (`conquistas.ts` + `store.ts`).

### Numeração

Por padrão, **renumere** para manter arquivos, ids, chaves de i18n e de
`suspendData` sequenciais e iguais à ordem na tela. Renumere de trás para
frente para não sobrescrever arquivos (`git mv secao-12.vue secao-13.vue`,
depois a 11 → 12…), e atualize em conjunto: imports, `id`, chaves do JSON (e
seus usos nos `.vue`), chaves do store, ids de conquista e catálogo. Depois,
`grep` pelos números antigos para garantir que nada ficou para trás.

### Progresso dos alunos (importante)

O `suspend_data` costuma ser validado por schema Zod
(`define-scorm-store.ts`); se não bater, **todo o progresso salvo é
descartado** e o aluno recomeça do zero. Remover chaves é tolerado;
adicionar chave nova, mudar tipo ou tamanho de tupla, ou renumerar chaves
invalida o progresso salvo (ou o atribui à seção errada).

- Se o curso **ainda não foi publicado** no LMS, renumere livremente e
  aumente `versao` em `definicao-curso.ts` (curso antigo:
  `app-definition.ts`) para limpar o `localStorage` de quem está testando.
- Se o curso **já tem alunos** no LMS, avise antes de aplicar e proponha a
  alternativa: manter as chaves antigas do store (sem renumerar o
  `suspendData`) ou aceitar o reset. Na dúvida sobre o status de
  publicação, pergunte.

### Adicionar

1. Crie o `.vue` a partir de um modelo existente (catálogo ou seção
   parecida).
2. Registre em `secoes.ts` na posição certa com a conclusão: `true` para
   estática, derivada do `suspendData` para interativa
   (`isSecaoConcluida.bool/array/tuple`), com `exibeTrava: true` nas
   interativas. Conteúdo que só aparece depois da interação fica na mesma
   seção, em `AppCoreExibeApos`.
3. Interativa: adicione o schema no `store.ts` no formato do componente
   (o `?catalogo` mostra o schema de cada um), seguindo as convenções do
   topo do arquivo (arrays pré-preenchidos, nunca vazios — `.every` de
   `[]` é `true`).
4. Textos no JSON, incluindo o título do menu.

### Remover

1. Apague o `.vue` (`git rm`), a entrada em `secoes.ts`, o import, a
   conclusão correspondente, as chaves do store (schema + initial) e as
   chaves do JSON.
2. Apague assets que só essa seção usava.
3. Renumere as seções seguintes (ver acima).

### Reordenar

Equivale a mover a entrada em `secoes.ts` (+ conclusão) e renumerar.
Confira se o texto das seções vizinhas não faz referência à ordem antiga
("na tela anterior…").

## 8. Verificação

Depois de aplicar os ajustes:

1. `npm run typecheck && npm run lint && npm run lint:css && npm run build && npm run build:validacao`
   (curso antigo: os scripts que existirem).
2. JSON válido e sem chaves órfãs ou faltando (`grep` das chaves
   alteradas e dos números antigos, se houve renumeração).
3. Mudança visual ou estrutural: confira no navegador as seções tocadas
   (desktop e celular; no tela a tela, a tela inteira sem corte, olhando).
4. Chame o agente `verificar-curso` no curso, dizendo quais seções
   mudaram (ele foca nelas e confere o resto por amostra, inclusive as
   travas sem `?liberar`). Traga os problemas que ele apontar para o
   retorno (seção 9) ou corrija os que forem do ajuste.

## 9. Retorno

Termine com um resumo por item, usando a numeração do arquivo de ajustes
(`S5.1`, `S5.2`…):

- ✅ aplicado — seção, chave/arquivo alterado
- 📋 aguardando aprovação — item estrutural incluído no planejamento
- ⚠️ aplicado com observação (ex.: placeholder no lugar da imagem, deslize
  de digitação normalizado, ocorrências não marcadas do mesmo termo,
  impacto no progresso)
- ❓ pendente — o que falta (asset, PDF novo) ou a dúvida que impede aplicar

Agrupe no fim o que depende do cliente/design (assets e PDFs a entregar,
perguntas), pronto para ser repassado.

### Checklist em arquivo

Além do resumo na conversa, salve o mesmo conteúdo como checklist em
Markdown **ao lado do arquivo de ajustes**, com o nome dele +
`-checklist.md` (ex.: `tmp/ajustes.pptx` → `tmp/ajustes-checklist.md`).
Confira com `git check-ignore` que o local está fora do git; se não
estiver, avise antes de criar. Estrutura:

1. Cabeçalho: arquivo de ajustes (e modelo, de `formatos-de-ajuste.md`),
   data, resultado da verificação (build/lint/JSON) e status do commit.
2. **Itens**: um por item `S<slide>.<caixa>`, na ordem do arquivo, como
   caixa de seleção (`- [x]` aplicado / `- [ ]` aguardando ou pendente), com
   o emoji de status, seção, chave/arquivo e antes → depois resumido.
   Separe num item próprio a parte que ficou pendente de um item aplicado
   pela metade (ex.: título trocado, mas imagem aguardando asset).
3. **Plano dos itens estruturais**: uma subseção por item, com o conteúdo
   do planejamento (seção 2), incluindo os textos a confirmar.
4. **Observações**: ocorrências não marcadas, deslizes normalizados,
   impacto no progresso, rastreabilidade (e-mails, pessoas, datas).
5. **Para repassar ao cliente/design**: checklist de assets, PDFs e
   perguntas.

Atualize o arquivo a cada rodada (aprovação, assets entregues): marque os
itens concluídos em vez de recriar a lista do zero.

Não faça commit sem que peçam. Quando pedirem, siga o estilo de mensagem do
histórico do projeto (`git log --oneline`).
