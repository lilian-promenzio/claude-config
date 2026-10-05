# claude-config

Configuração global do Claude Code (`~/.claude`) versionada: skills e
settings.

## Conteúdo

| Caminho | O quê |
| ------- | ----- |
| `settings.json` | Preferências globais (tema, nível de esforço, notificações) e permissões genéricas. |
| `skills/ajustes-curso/` | Aplica ajustes de cliente/revisão em cursos Plural (Vue + SCORM) a partir de um `.pptx` de ajustes. Inclui o extrator de pptx e o catálogo de formatos de arquivo de ajustes. |

## Instalação

```sh
git clone <url-deste-repo> ~/Projetos/claude-config
~/Projetos/claude-config/instalar.sh
```

O script cria links simbólicos de `~/.claude/settings.json` e
`~/.claude/skills/<skill>` para este repositório. O que já existir no lugar
é movido para `~/.claude/backups/claude-config-<data>/`. Pode ser rodado de
novo sem problema.

Com os links, qualquer alteração feita pelo Claude Code numa skill ou no
settings já aparece aqui — é só revisar com `git diff` e commitar.

Dependências da skill `ajustes-curso`: `python3` (Pillow opcional, para
recortar imagens), LibreOffice (`soffice`, para renderizar o pptx em PDF) e
ImageMagick (`magick`, para gerar placeholder de imagem).

## Cuidados

- **Permissões**: ao aprovar "sempre permitir" uma ação, o Claude Code grava
  a regra em `settings.json` — ou seja, aqui. Antes de commitar, revise o
  `git diff` e mantenha só regras genéricas (ex.: `Bash(npm install *)`).
  Regras de um projeto específico pertencem ao `.claude/settings.local.json`
  do projeto.
- **Link substituído**: se algum programa regravar `~/.claude/settings.json`
  como arquivo comum, o link se perde. Rode `./instalar.sh` — ele avisa se o
  conteúdo diferia e guarda a cópia no backup.
- **Nunca versionar**: `.credentials.json` (token de login), `history.jsonl`
  e `projects/` (conversas, com material de clientes). O `.gitignore` bloqueia
  esses nomes como rede de segurança.
- `skills/synced/` e `plugins/` são geridos pela conta claude.ai e pelo
  marketplace — não entram aqui.
