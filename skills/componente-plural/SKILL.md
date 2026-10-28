---
name: componente-plural
description: Cria ou altera um componente da biblioteca plural/ (ou um bloco de plural/layout/) da plural-curso-base, do começo ao fim — convenções, catálogo, CHANGELOG, versão e verificação — e leva para a base uma lacuna encontrada num curso. Use quando pedirem um componente novo ou uma opção nova num componente da plural/ (ex.: "criar o PluralSequencia", "feedback em modal nos exercícios", "levar a abertura EBANX para a base").
argument-hint: "[componente ou lacuna]"
---

# Componente da `plural/`

Pedido: $ARGUMENTS

As regras estão na `src/plural/CONVENCOES.md` da base
(`~/Projetos/Plural/modelos/plural-curso-base`) — **leia-a inteira antes de
escrever**. Esta skill só dá a ordem dos passos e o que costuma ser
esquecido.

## 1. Onde vai

- Genérico, serve a outros cursos → `src/plural/` (bloco de seção ou tela →
  `src/plural/layout/`).
- Identidade de um cliente sobre um componente que já existe → wrapper
  `App*` no curso, só com variáveis CSS (`docs/guia-wrapper-app.md`). Não é
  com esta skill.
- Só faz sentido num curso → `src/components/` do curso.

**Dentro de um curso, não edite a `plural/` nem o `core/`** (são copiados
da base e voltam a divergir). Se faltar algo genérico, resolva no curso com
um componente próprio, registre a lacuna (o que falta e onde foi
contornado) e faça a versão genérica na base com esta skill.

## 2. Antes de escrever

- Procure algo parecido no `?catalogo`: estender um componente é melhor
  que criar outro.
- Vindo de um curso: leia o componente de lá **inteiro** (inclusive os
  ajustes já feitos com o cliente) e separe o que é identidade (cores,
  imagens, textos, layout do cliente) do que é comportamento genérico. Só o
  genérico vem para a base.
- Leia o modelo citado na `CONVENCOES.md` (flip card) e um componente
  parecido com o novo (ex.: para exercício, `plural-questao.vue` e
  `use-exercicio.ts`).

## 3. Escrever

Pela `CONVENCOES.md`, item a item. O que mais se esquece:

- Comentário do topo: o que faz, formato do `v-model` **e o schema do
  suspendData**, `@example`, lista de variáveis CSS com o padrão de cada uma.
- Visual só por variáveis CSS com fallback em **token semântico**
  (`primary`, `accent`, `superficie`, `texto`…) — nunca nome de paleta nem
  cor solta (o stylelint barra). Props só para estrutura e comportamento.
- Instrução (slot com padrão + prop), estados (`data-estado`), indicador,
  textos internos com padrão em `src/plural/locales/pt-BR.json` e prop
  `rotulo*` para trocar.
- Layout por `@container`; ponteiro dividido por `useEscala()`; modais e
  balões pela camada flutuante; nada de `v-entrada` dentro da `plural/`.
- Exercícios: `useExercicio`, tentativas, gabarito; props com
  `& OpcoesResultadoExercicio` e `...PADROES_RESULTADO` (feedback abaixo ou
  em modal, rótulos dos botões), repassadas **uma a uma** ao
  `PluralExercicioResultado` (por função, o `vue/no-unused-properties` não
  as enxerga); espaçamentos só pelas variáveis `--exercicio-*`, com o valor
  atual como reserva, para a classe `plural-exercicio-compacto` valer.
- Acessibilidade: teclado, foco visível, `aria-*`, `prefers-reduced-motion`.

Legibilidade (o lint não pega): `if` em bloco em vez de ternário composto;
`computed` antes de `watch`; nada de estado duplicado que possa divergir;
`provide/inject` só com `InjectionKey` tipada; funções pequenas com nome
que diz o que fazem; nomes em português.

## 4. Catálogo

- Entrada em `src/catalogo/catalogo-dados.ts`: v-model, props, slots,
  estados, variáveis CSS, schema do suspendData.
- Demo em `src/catalogo/demos/demo-<grupo>.vue`: uso padrão, variações
  relevantes, identidade aplicada só por variáveis. Cores das demos só
  semânticas ou de `CORES_DO_CURSO`.

## 5. Versão

Registre no `src/plural/CHANGELOG.md` (o que mudou e, se quebra o uso,
como migrar) e suba `src/plural/versao.ts` pela regra do topo do CHANGELOG.
Se houver uma seção "Próxima versão" aberta (etapa em andamento), registre
nela e não suba a versão.

## 6. Verificar

```sh
npm run lint && npm run lint:css && npm run typecheck && npm run verificar:esqueleto
```

- Abra a demo no `?catalogo` (dev): confira visual, teclado e, quando fizer
  diferença, o uso numa seção de rolagem e numa tela do tela a tela
  (`?formato=`). Interações dá para testar com Playwright clicando pelos
  nomes acessíveis (bom teste de acessibilidade também).
- No tela a tela, confira o corte **olhando**: o aviso do console só pega o
  que passa da tela, não o que um bloco recorta por dentro.
- Chame o agente `revisor-convencoes` sobre o diff e corrija o que for de
  "Corrigir"; traga os "Considerar" ao usuário.
- No relatório: o que foi feito, o que foi verificado (com os resultados
  dos comandos) e o que ficou pendente.
