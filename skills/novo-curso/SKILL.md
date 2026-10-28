---
name: novo-curso
description: Cria um novo curso e-learning SCORM da Plural (Vue 3 + TS + Tailwind v4 + Vite) a partir do material do cliente — roteiro (.pptx), imagem de layout, branding (PDF) e assets — partindo da plural-curso-base (ou de outro curso do mesmo cliente). Use quando pedirem para "criar um curso novo", "começar o curso do cliente X", "montar o projeto a partir do roteiro/layout" ou para iniciar uma nova peça/trilha.
argument-hint: "[pasta do curso novo] [curso de origem, se não for a base]"
---

# Novo curso SCORM

Você vai construir um curso novo a partir do material do cliente. O que mais
gera retrabalho não é o código: é **ler mal o layout** (divisão de seções,
posição de caixas, cantos, sombras, cores) e **não ser fiel ao roteiro**
(hierarquia, negrito, itálico, sublinhado, maiúsculas). Esta skill existe para
acertar isso de primeira.

Argumentos: $ARGUMENTS

Base: `~/Projetos/Plural/modelos/plural-curso-base` (se não estiver lá,
pergunte onde está). Arquivos de apoio em `~/.claude/skills/novo-curso/`:

- `referencias/perguntas-iniciais.md` — questionário da definição do curso.
- `referencias/licoes-de-layout.md` — **checklist de leitura do layout e do
  roteiro**, com os erros já corrigidos em revisões de clientes. Ler antes de
  desenhar o mapa de seções e de novo antes de entregar.
- `scripts/extrair-roteiro.py` — roteiro .pptx → Markdown com a formatação em
  HTML (`<strong>`, `<em>`, `<u>`, caixa alta de estilo, tamanhos, listas).
- `scripts/capturar-secoes.mjs` — captura cada seção (rolagem, em desktop e
  celular) ou cada tela (tela a tela) para comparar com o layout.

## 0. Origem do projeto

- **C. Base Plural (padrão).** O curso nasce da `plural-curso-base`.
- **B. Mesma identidade.** Trilha/peça de um cliente que já tem curso **feito
  da base**: parte desse curso (tema, `components/`, `App.vue`, fontes);
  conteúdo e configuração vêm vazios do esqueleto da base.
- **A. Referência manual.** Só quando o usuário pedir, ou para um cliente
  cujo curso é anterior à base: copiar o curso indicado e limpar à mão
  (views, locales, assets, config de seções/store/menu; nome, chave do
  localStorage, `imsmanifest.xml`). Leia o `CLAUDE.md`, o `README.md` e o
  catálogo da referência antes; registre no `CLAUDE.md` novo de onde veio
  cada parte. O resto desta skill vale com os nomes daquele curso.

Na dúvida entre B e C (o cliente tem curso?), pergunte.

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

Asset faltando → `PluralPlaceholder` (ou o placeholder dos blocos de layout)
e anote para o designer. Não invente ilustrações nem textos.

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
- Menu lateral do roteiro (se houver) → itens do menu do curso.
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

## 4. Definição do curso e mapa de seções — CHECKPOINT

1. **Definição**: aplique `referencias/perguntas-iniciais.md` (deduza o que
   der do material; pergunte o resto).
2. **Mapa** (menu | seção | slide | conteúdo | interação/trava): apresente
   ao usuário **antes de construir**, com as dúvidas (textos suspeitos do
   roteiro, assets faltando, slides sem layout).

Regras do mapa:

- **Um bloco visual do layout = uma seção** (fundo e espaçamento próprios).
  Um slide do roteiro pode virar várias seções, ou várias partes de slides uma
  seção só. **Tela a tela**: uma tela = uma seção, que cabe em 1280 × 720.
- Toda seção com interação **trava as seguintes** até ser concluída.
- Conteúdo do **mesmo bloco** que só deve aparecer após a interação (caixa de
  fechamento abaixo de um acordeão, texto após um fluxo) fica **na mesma
  seção**, com `AppCoreExibeApos` — não vira seção.
- Só vira seção nova o que é **visualmente apartado** (outra cor de fundo,
  foto de largura total, faixa). Nunca simule continuidade reduzindo o
  espaçamento entre duas seções.

## 5. Construir

1. **Criar o projeto** (modos C e B), com a definição em
   `<scratchpad>/definicao.json`:

   ```sh
   BASE=~/Projetos/Plural/modelos/plural-curso-base
   node $BASE/scripts/criar-curso.mjs <pasta-do-curso> --nome "Nome" --slug cliente-curso \
     --definicao <scratchpad>/definicao.json [--origem <curso-do-cliente>]
   ```

   Copia o último commit da base (se ela tiver mudanças locais, avisa: pare
   e pergunte), tira o que é só da base, troca o conteúdo pelo curso vazio,
   aplica nome/chave/definição, instala e roda typecheck, lint e build. Só
   siga com tudo ok. A pasta pode já ter `tmp/` com o material.
2. Leia o `CLAUDE.md` do curso criado: é a fonte das regras (camadas, o que
   não editar, tokens, tela a tela). Acrescente nele a seção "Course
   definition" (respostas do questionário) e as regras de estilo do cliente
   (paleta, cantos, sombras, fontes).
3. **Tema** (`src/assets/styles/tema.css`): paleta do branding com nomes em
   português, aliases semânticos, fontes, `--radius-*`, `--shadow-*`,
   espaçamentos — já com os valores lidos do layout. Logo nos slots do
   `AppCasca` (`App.vue`).
4. **Componentes**: procure no `?catalogo` antes de criar. Identidade do
   cliente em wrappers `App*` (`docs/guia-wrapper-app.md`); não edite
   `src/plural/` nem `src/core/` — se faltar algo genérico, anote para levar
   à base.
5. **Textos** em `src/assets/locales/pt-BR.json` (`mNN-sNN-…`), copiados do
   Markdown do roteiro com a formatação HTML.
6. **Seções, módulos e travas** pelo `docs/guia-conteudo.md` do curso,
   seguindo o mapa aprovado. Atualize o mapa das seções no `README.md`.

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

- Captura o módulo atual; com vários módulos, troque de módulo no navegador
  e rode de novo.
- Compare **cada captura com o trecho correspondente do layout**, passando
  pelo checklist de `referencias/licoes-de-layout.md`.
- Teste as travas **sem** `?liberar`: seção seguinte oculta (ou "avançar"
  bloqueado) até concluir a interação; conteúdo condicional só aparece
  depois; menu libera os links; o progresso anda e sobrevive a recarregar.
- Rolagem: celular (390px) sem rolagem horizontal, texto fora das áreas
  decorativas, nada cortado. Tela a tela: nenhuma tela cortada (o console
  avisa).
- Teclado e leitor de tela: foco visível, interações operáveis por teclado,
  `alt` nas ilustrações com personagem, decorativas com `alt=""`.

Antes de entregar, chame o agente `verificar-curso` no curso (com o
caminho do layout): ele refaz tudo isso num contexto separado e devolve
só o relatório. Corrija o que ele apontar.

## 7. Entregar

Relatório final ao usuário:

- o que foi feito e verificado (com os resultados reais dos comandos);
- pedidos específicos atendidos (lista do passo 1);
- **pendências para o cliente/designer**: textos suspeitos do roteiro,
  assets em placeholder, slides sem layout, decisões tomadas por falta de
  referência;
- o que pareceu faltar na base (componente, variante, opção da definição).

Se durante o projeto o usuário corrigir algo que valha para cursos futuros,
proponha acrescentar o ponto em `referencias/licoes-de-layout.md`.
