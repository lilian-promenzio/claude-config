#!/usr/bin/env bash
# Liga as configurações deste repositório ao ~/.claude por links simbólicos.
# Pode ser rodado de novo a qualquer momento (ex.: após adicionar uma skill
# ou se algum link tiver sido substituído por arquivo comum).
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
BACKUP="$CLAUDE_DIR/backups/claude-config-$(date +%Y%m%d-%H%M%S)"

# Cria o link `destino` -> `origem`. Se já existir um arquivo/pasta comum no
# destino, move para o backup antes (e avisa se o conteúdo era diferente).
ligar() {
	local origem="$1" destino="$2"
	if [ -L "$destino" ] && [ "$(readlink "$destino")" = "$origem" ]; then
		echo "ok        $destino"
		return
	fi
	if [ -e "$destino" ] || [ -L "$destino" ]; then
		if ! diff -rq "$origem" "$destino" >/dev/null 2>&1; then
			echo "ATENÇÃO   $destino difere do repositório — cópia guardada no backup:"
			diff -ru "$origem" "$destino" | head -20 || true
		fi
		mkdir -p "$BACKUP"
		mv "$destino" "$BACKUP/"
	fi
	mkdir -p "$(dirname "$destino")"
	ln -s "$origem" "$destino"
	echo "ligado    $destino -> $origem"
}

ligar "$REPO/settings.json" "$CLAUDE_DIR/settings.json"

for skill in "$REPO"/skills/*/; do
	skill="${skill%/}"
	ligar "$skill" "$CLAUDE_DIR/skills/$(basename "$skill")"
done

[ -d "$BACKUP" ] && echo "Backup do que foi substituído: $BACKUP"
exit 0
