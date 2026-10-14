---
name: novo-curso
description: Cria um novo curso e-learning SCORM da Plural (Vue 3 + TS + Tailwind v4 + Vite) a partir do material do cliente — roteiro (.pptx), imagem de layout, branding (PDF) e assets — usando um projeto de referência como base. Use quando pedirem para "criar um curso novo", "começar o curso do cliente X", "montar o projeto a partir do roteiro/layout" ou para iniciar uma nova peça/trilha.
argument-hint: "[caminho do projeto de referência]"
---

# Novo curso SCORM

Você vai construir um curso novo a partir do material do cliente. O que mais
gera retrabalho não é o código: é **ler mal o layout** (divisão de seções,
posição de caixas, cantos, sombras, cores) e **não ser fiel ao roteiro**
(hierarquia, negrito, itálico, sublinhado, maiúsculas). Esta skill existe para
acertar isso de primeira.

Referência informada: $ARGUMENTS

Arquivos de apoio (em `~/.claude/skills/novo-curso/`):

- `referencias/licoes-de-layout.md` — **checklist de leitura do layout e do
  roteiro**, com os erros já corrigidos em revisões de clientes. Ler antes de
  desenhar o mapa de seções e de novo antes de entregar.
- `referencias/perguntas-iniciais.md` — questionário de definições do curso
  (navegação, menus, plugins…). **Futuro**: só usar quando houver a base
  genérica (ver passo 0).
- `referencias/arquitetura.md` — estrutura-alvo do projeto (camadas
  plural/components/core/config, travas, menu, `?liberar`, catálogo).
- `scripts/extrair-roteiro.py` — roteiro .pptx → Markdown com a formatação em
  HTML (`<strong>`, `<em>`, `<u>`, caixa alta de estilo, tamanhos, listas).
- `scripts/capturar-secoes.mjs` — captura cada seção em desktop e celular
  (Playwright) para comparar com o layout.

## 0. Origem do projeto

Defina de onde o projeto parte. **Hoje só o modo A está ativo.**

- **A. Referência manual (atual).** O usuário indica um ou mais cursos
  existentes (`$ARGUMENTS` ou a mensagem). Se não indicou, **pergunte** — não
  escolha sozinho. Pode haver papéis diferentes, por exemplo:
  - base principal (estrutura, camadas, catálogo, core SCORM);
  - mecânicas pontuais de outro curso (ex.: `?liberar` + build de
    validação, menu lateral com progresso);
  - curso para consulta de componentes antes de criar um novo.
  Registre no `CLAUDE.md` do novo projeto de onde veio cada parte.
- **B. Mesma identidade (futuro).** Trilha/peça de um cliente que já tem
  curso: partir desse curso, reaproveitando tema, componentes `App*` e
  padrões de layout; só o conteúdo muda.
- **C. Base Plural (futuro).** Partir do projeto base consolidado, com a
  biblioteca `plural` completa; criar o tema do cliente do zero.

> Quando a base existir, este passo passa a oferecer B/C e o restante desta
> skill continua valendo.

**Definições do curso (futuro, junto com o modo C).** Antes de criar o
projeto, aplicar o questionário de `referencias/perguntas-iniciais.md`:
navegação (one page, multipage ou tela a tela), menu de âncoras flutuante,
menu lateral com progresso, plugin de acessibilidade, VLibras, critério de
conclusão etc. As respostas definem quais recursos da base entram no
projeto. **Enquanto só o modo A existir, não aplique o questionário**: os
recursos vêm da referência indicada.

Leia o `CLAUDE.md`, o `README.md` e o catálogo (`src/catalogo/`) de cada
referência antes de copiar qualquer coisa.

## 1. Material e pedidos do curso

Confirme que existe (normalmente em `tmp/`, fora do git):

| Material | Papel |
| --- | --- |
| roteiro (.pptx) | **fonte de verdade de TODO texto** e das interações/travas |
| layout (imagem) | composição, cantos, sombras, espaçamentos, divisão de blocos — **não** de textos nem de tons de cor |
| branding (PDF) | paleta (anote a página) e tipografia |
| ícones, ilustrações, fotos, vídeo, áudio, fontes | assets |

Separe também os **pedidos específicos** da mensagem do usuário (ex.: "inserir
podcast no slide 20 com plural-wavesurfer", "menu lateral colapsável") e
liste-os — eles entram no relatório final como itens verificados.

Asset faltando → placeholder visível e anote para o designer. Não invente
ilustrações nem textos.

## 2. Ler o roteiro

```sh
python3 ~/.claude/skills/novo-curso/scripts/extrair-roteiro.py tmp/roteiro.pptx > <scratchpad>/roteiro.md
soffice --headless --convert-to pdf --outdir <scratchpad> tmp/roteiro.pptx   # leitura visual
```

- O Markdown é a fonte para copiar texto: já vem com `<strong>/<em>/<u>`,
  caixa alta de estilo convertida (`[caps]`) e tamanhos (`[24pt]`) que
  indicam a hierarquia. Confira a hierarquia no PDF (estilos herdados do
  mestre não aparecem no extrator).
- Separe conteúdo de **instruções de produção** (caixas "ORIENTAÇÃO PARA
  PRODUÇÃO", "INTERAÇÃO: …", "SÓ LIBERAR AVANÇO APÓS…", nomes de asset como
  `ICON_05_02`, `IMG_SLIDE_20`, links do OneDrive/Figma). As instruções viram
  comportamento; nunca texto na tela.
- Menu lateral do roteiro (se houver) → grupos do menu do curso.
- Erros de digitação/concordância no roteiro: **não corrija em silêncio**;
  mantenha e liste no relatório para o cliente confirmar.

## 3. Ler o branding e o layout

- Branding: extraia a paleta **exata** (hex) e as fontes. Converta fontes para
  WOFF2 se vierem em TTF/OTF.
- Layout: a imagem costuma ser gerada por IA. Use para **estrutura**: blocos,
  fundos, onde uma faixa de cor termina, lado de cada caixa, alinhamentos,
  cantos, presença ou não de sombra/borda. Amplie por trechos para ver
  detalhes (`magick layout.png -crop 100%x12% +repage <scratchpad>/layout-%02d.png`).
- **Cores: só as do branding.** O layout mistura tons; mapeie cada tom para o
  nome mais próximo da paleta e nunca crie tons intermediários.

Leia agora `referencias/licoes-de-layout.md` inteiro.

## 4. Mapa de seções — CHECKPOINT

Monte a tabela do mapa (menu | seção | slide | conteúdo | interação/trava) e
**apresente ao usuário antes de construir as seções**, junto com as dúvidas
(textos suspeitos do roteiro, assets faltando, slides sem layout).

Regras:

- **Um bloco visual do layout = uma seção** (fundo e espaçamento próprios).
  Um slide do roteiro pode virar várias seções, ou várias partes de slides uma
  seção só.
- Toda seção com interação **trava as seguintes** até ser concluída.
- Conteúdo do **mesmo bloco** que só deve aparecer após a interação (caixa de
  fechamento abaixo de um acordeão, texto após um fluxo) fica **na mesma
  seção**, com exibição condicional (`AppCoreExibeApos`) — não vira seção.
- Só vira seção nova o que é **visualmente apartado** (outra cor de fundo,
  foto de largura total, faixa). Nunca simule continuidade reduzindo o
  espaçamento entre duas seções.

## 5. Construir

Ordem recomendada (detalhes em `referencias/arquitetura.md`):

1. **Scaffold** a partir da referência: copiar estrutura, limpar conteúdo do
   curso antigo (views, locales, assets, config de seções/store/menu), ajustar
   `package.json`, `app-definition.ts` (nome, `localStorageName`, `versao`),
   `imsmanifest.xml`, título. Instalar e garantir que `dev`/`build` sobem
   vazios antes de seguir.
2. **Tema** (`tema.css`): paleta do branding com nomes em português, aliases
   semânticos, fontes, `--radius-*`, `--shadow-*`, espaçamentos — já com os
   valores lidos do layout (cantos pequenos? sem sombra?).
3. **Componentes**: consulte o catálogo das referências antes de criar.
   Genérico em `src/plural` (customizável por CSS custom properties com
   fallback em tokens, documentadas no topo do arquivo); identidade do cliente
   em `src/components` (`App*` que só definem as variáveis, mais os blocos de
   layout). Todo componente reutilizável ganha entrada + demo no catálogo.
4. **Textos** em `src/assets/locales/pt-BR.json` (`mNN-sNN-…`), copiados do
   Markdown do roteiro com a formatação HTML.
5. **Seções** (`views/modulo-N/secao-M.vue`), seguindo o mapa aprovado.
6. **Mecânicas**: `store.ts` (uma chave por seção interativa), `secoes.ts`
   (travas), menu lateral + progresso, `?liberar` + `build:validacao`,
   conclusão SCORM na última seção.

Trabalhe por blocos de seções e verifique cada bloco (passo 6) antes de
seguir — erro de padrão visual repetido em 30 seções custa caro.

## 6. Verificar

```sh
npm run typecheck && npm run lint && npm run lint:css && npm run build && npm run build:validacao
```

Visual, com o dev server rodando:

```sh
# numa pasta do scratchpad com `npm i playwright`, copiando o script para lá
node capturar-secoes.mjs "http://localhost:<porta>/?liberar" <scratchpad>/capturas 1280,390
```

- Compare **cada captura com o trecho correspondente do layout**, passando
  pelo checklist de `referencias/licoes-de-layout.md`.
- Teste as travas **sem** `?liberar`: seção seguinte oculta até concluir a
  interação; conteúdo condicional só aparece depois; menu libera os links; a
  barra de progresso anda; o progresso sobrevive a recarregar a página.
- Celular (390px): sem rolagem horizontal, texto fora das áreas decorativas,
  nada cortado.
- Teclado e leitor de tela: foco visível, interações operáveis por teclado,
  `alt` nas ilustrações com personagem, decorativas com `alt=""`.

## 7. Documentar e entregar

- `README.md`: comandos, mapa das seções (marcar conteúdo condicional),
  tokens.
- `CLAUDE.md` do projeto: origem (referências usadas), regras de estilo do
  cliente (paleta, cantos, sombras, fontes), camadas, estrutura do curso.
- Relatório final ao usuário:
  - o que foi feito e verificado (com os resultados reais dos comandos);
  - pedidos específicos atendidos (lista do passo 1);
  - **pendências para o cliente/designer**: textos suspeitos do roteiro,
    assets em placeholder, slides sem layout, decisões tomadas por falta de
    referência.

Se durante o projeto o usuário corrigir algo que valha para cursos futuros,
proponha acrescentar o ponto em `referencias/licoes-de-layout.md`.
