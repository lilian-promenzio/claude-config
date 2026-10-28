---
name: atualizar-plural
description: Atualiza um curso feito da plural-curso-base para a versão atual da base — troca src/plural/, src/core/ e configs pelo script da base e aplica a migração nos arquivos do curso (estilos, views, wrappers) pelo CHANGELOG. Use quando pedirem para atualizar a plural/ ou a base de um curso ("levar a 1.1.0 para a CLARO", "atualizar o curso para a base nova").
argument-hint: "[pasta do curso]"
---

# Atualizar um curso para a base atual

Curso: $ARGUMENTS

Base: `~/Projetos/Plural/modelos/plural-curso-base`. O curso registra de
onde veio na seção "Origin" do seu `CLAUDE.md` (commit da base e versão da
`plural/`).

## 1. Antes

- Curso com git: árvore limpa (`git status`); se não, peça para commitar
  antes. Sem git: copie o curso (sem `node_modules`/`dist*`) para o
  scratchpad, para poder voltar.
- **Capture o curso antes** (`capturar-secoes.mjs` da skill `novo-curso`,
  desktop e celular ou cada tela), numa pasta do scratchpad: é o "antes"
  que o `verificar-curso` compara depois.
- Base: o que entra é o **último commit**; mudanças não commitadas ficam
  de fora.
- Curso criado de outro curso do cliente (modo B): o "Origin" não tem o
  commit da base. Descubra pela versão da `plural/` (o commit da base em
  que `src/plural/versao.ts` passou a ter aquela versão) e passe `--de`.

## 2. Rodar o script

```sh
node ~/Projetos/Plural/modelos/plural-curso-base/scripts/atualizar-curso.mjs <curso>
```

Troca o que o curso não edita (`src/plural/`, `src/core/`, `src/catalogo/`,
`DEFINICAO-CURSO.md`, configs de lint e TypeScript, `.claude/`), junta as
dependências da base no `package.json`, atualiza o "Origin", roda install e
as verificações, e escreve `<curso>/.atualizacao-plural/RELATORIO.md`.
Leia o relatório inteiro. A "Verificação" dele é a de **antes** da
migração (erros de lint ali são esperados).

## 3. Migração

Leia no `src/plural/CHANGELOG.md` (já o novo, no curso) todas as versões
entre a antiga e a nova, em especial as linhas **Migração**. Depois:

1. **Alterados no curso e trocados** (`backup/`): o curso tinha mexido na
   `plural/` ou no `core/`. Compare o backup com a versão nova. Se a
   mudança ainda for necessária, refaça-a **fora** da `plural/` (wrapper
   `App*`, componente do curso, variável CSS) e registre a lacuna para a
   base (skill `componente-plural`). Nunca copie o backup de volta.
2. **Conflitos** (`base/`): arquivo de configuração que o curso alterou.
   Junte à mão as duas versões (a do curso e a de `base/`).
3. **Migração** (`migracao.diff`): o que mudou na base em arquivos do curso
   (estilos, `App.vue`, guias, `CLAUDE.md`, `esqueleto/` — o esqueleto
   mostra as mudanças em `src/config/` e nas views). Aplique o que vale
   para o curso; não copie conteúdo do exemplo.
4. **Verificações que falharam**: `npm run lint:fix` primeiro; o resto à
   mão, pela regra que o erro cita (`CLAUDE.md` do curso). Casos comuns:
   slots sem `defineSlots` nos wrappers; `rgb()`/hex → `color-mix` com um
   token (`color-mix(in srgb, var(--color-preto) 35%, transparent)`);
   `:deep()` em texto `v-html` → `<style>` sem `scoped` em
   `@layer components` (`docs/guia-wrapper-app.md`).
5. **Opcional**: o que a versão nova resolve e o curso contornava (linha
   "Opcional" do CHANGELOG, lacunas registradas no curso). Aplique só o
   que for igual ao layout/roteiro do curso, e diga no relatório.

## 4. Verificar e fechar

- `npm run typecheck && npm run lint && npm run lint:css && npm run build && npm run build:validacao`
- Abra no navegador as seções que usam componentes que mudaram (o
  CHANGELOG diz quais) e compare com antes (capturas do curso antes da
  atualização, se houver, ou a versão publicada).
- Chame o agente `verificar-curso` no curso, com a pasta das capturas de
  antes e o que mudou (CHANGELOG e migração), para ele comparar.
- Apague `<curso>/.atualizacao-plural/`.
- Relatório: versões (de → para), o que foi migrado, lacunas levadas à
  base, o que o `verificar-curso` apontou e o que ficou pendente.

Commit só quando o usuário pedir.
