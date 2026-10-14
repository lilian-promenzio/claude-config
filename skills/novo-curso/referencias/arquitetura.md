# Arquitetura-alvo de um curso Plural

Estado de referência: curso EBANX LD/FT
(`clientes/insight/ebanx/compliance`, out/2026), que juntou a `_base` da
EntrePares (`clientes/fundacao-itau/entre-pares/_base`), o `?liberar` do
`clientes/claro/trilha-da-qualidade/multipage` e o menu lateral do
`clientes/insight/bp-bioenergy/conversa-pre-trabalho`. Se a referência
indicada pelo usuário divergir disto, **a referência vence**; use este
arquivo para saber o que procurar nela e o que não pode faltar.

Stack: Vue 3 + TypeScript + Tailwind v4 + Vite, SCORM 1.2, vue-i18n, Pinia,
Zod + msgpack no `suspend_data`, AOS, Plyr (vídeo), wavesurfer.js (áudio).

## Pastas

```
src/
  plural/            genéricos, sem identidade de cliente
    plural-tokens.css  valores neutros dos tokens
  components/        App* do cliente: aplicam a identidade + blocos de layout
    cores.ts           CORES_CAIXA: mapa bg+texto para toda prop `cor`
  core/              SCORM, curso, validação, componentes de orquestração
    curso.ts           montarSecoes, acumulaDesbloqueio (honra ?liberar)
    validacao.ts       IS_BUILD_VALIDACAO, TRAVAS_LIBERADAS
    criar-curso.ts     bootstrap (i18n, pinia, chave do localStorage)
    scorm/             API SCORM, isSecaoConcluida.bool/array/tuple
    componentes/       AppCoreSecoes, AppCoreTravaAviso, AppCoreExibeApos,
                       AppCoreConcluiAoAparecer, AppCursoLayout…
  config/
    app-definition.ts  nome, localStorageName, versao (subir zera progresso)
    modulos.ts, secoes.ts, store.ts, menu.ts, contatos.ts…
  views/modulo-N/secao-M.vue   uma seção por arquivo
  assets/
    locales/pt-BR.json   todos os textos (mNN-sNN-…; HTML com v-html)
    styles/              estilos.css (entrada), tema.css, global.css,
                         fontes.css, animacoes.css
    img/icones/          icon-NN-NN.svg (nome do ICON_NN_NN do roteiro)
  catalogo/          /?catalogo em dev: fundamentos, blocos, componentes
public/imsmanifest.xml
```

## Camadas de componentes

- `plural/*`: comportamento + estrutura. Toda cor, raio, sombra e espaçamento
  vem de CSS custom properties com fallback em token, **documentadas no
  comentário do topo** (`--questao-opcao-bg … padrão --color-superficie-alt`).
  Variantes de comportamento por prop (ex.: `gabarito="cores" | "selos"`).
- `components/App*`: definem as variáveis do plural correspondente e trazem
  os blocos de layout do cliente (abertura, título, foto com caixa, faixa…).
  Não duplicar lógica do plural; se faltar algo, estender o plural.
- Variantes visuais por `data-*` (`data-variante`, `data-layout`), não por
  classes concatenadas.
- Todo componente reutilizável: entrada em `catalogo-dados.ts` + demo.

## Tema (`tema.css`)

`@theme static` com:

- paleta do branding com nomes em português (`--color-azul`…), e aliases
  semânticos (`--color-primary`, `--color-texto`, `--color-sucesso`,
  `--color-erro`, `--color-foco`…);
- `--radius-caixa`, `--radius-controle`, `--radius-botao`;
- `--shadow-caixa` (frequentemente `none`), `--shadow-flutuante` (menu,
  botões fixos);
- `--spacing-caixa`, `--spacing-caixa-compacta`;
- `--font-titulo`, `--font-destaque`, `--font-texto`;
- layout: `--container-largura-max`, `--menu-lateral-largura`.

Ícones do designer: `PluralIconeMascara` + `icone("NN-NN")` pintam o SVG com
`mask-image` na cor do texto. Ícone com partes brancas → converter as partes
em furos reais (`<mask>` no SVG), senão vira disco sólido. Se o layout pede
só o traço de um ícone entregue como disco vazado, gerar uma variante
`icon-NN-NN-traco.svg`.

## Curso, travas e progresso

- `store.ts`: schema Zod do `suspend_data`, **uma chave por seção
  interativa** (`bool` para vídeo/áudio/visualização, `array` de bool para
  itens clicados, `string[]` para respostas, `tuple` para combinações).
  `isComplete` aponta a conclusão da última seção.
- `secoes.ts`: `montarSecoes([[Componente, concluida, { exibeTrava: true }], …])`;
  seções sem interação não travam.
- Conteúdo condicional dentro da seção:
  `<AppCoreExibeApos :concluida="isSecaoConcluida.array(sd.m01.s15)">`.
- Última seção: `AppCoreConcluiAoAparecer` → SCORM `completed`.
- `menu.ts`: grupos do menu lateral (itens do roteiro) apontando para a
  primeira seção de cada tema; link liberado quando a seção é desbloqueada;
  progresso = seções liberadas e concluídas ÷ total.

## Validação com o cliente

- `?liberar` libera todas as seções e links (só em dev e no modo Vite
  `validacao`; no build SCORM vira `false` em tempo de compilação).
- `npm run build:validacao` → `dist-validacao/`, chave do localStorage com
  sufixo `_validacao`. Adicionar `dist-validacao` aos ignores do eslint e do
  stylelint.

## Scripts esperados no package.json

`dev`, `build` (`vue-tsc -b && vite build`), `build:validacao`
(`… --mode validacao --outDir dist-validacao`), `typecheck`, `preview`,
`lint`, `lint:fix`, `lint:css`.
