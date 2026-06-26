#!/usr/bin/env bash
# Hook guard de seguridad (PreToolUse) para Claude Code.
# Bloquea (exit 2) edits a archivos sensibles y comandos peligrosos.
# El stderr se le pasa a Claude como feedback para que proponga una alternativa.
#
# Instalar: ver hooks-ejemplo/settings.snippet.json
# Recordá: chmod +x hooks-ejemplo/guard.sh

input=$(cat)   # Claude pasa un JSON por stdin

tool=$(printf '%s' "$input" | python3 -c "import sys,json;print(json.load(sys.stdin).get('tool_name',''))")
args=$(printf '%s' "$input" | python3 -c "import sys,json;print(json.dumps(json.load(sys.stdin).get('tool_input',{})))")

# 1) Proteger archivos sensibles ante Edit/Write
if [ "$tool" = "Edit" ] || [ "$tool" = "Write" ]; then
  if printf '%s' "$args" | grep -Eq '(^|/)\.env($|"|/)|package-lock\.json|poetry\.lock|/migrations/'; then
    echo "BLOQUEADO: no se permite editar archivos sensibles (.env, lockfiles, migraciones). Pedí confirmación humana o usá .env.example." >&2
    exit 2
  fi
fi

# 2) Frenar comandos peligrosos en Bash
if [ "$tool" = "Bash" ]; then
  if printf '%s' "$args" | grep -Eq 'rm[[:space:]]+-rf|git[[:space:]]+push[[:space:]]+.*--force|git[[:space:]]+push[[:space:]]+.*-f([[:space:]]|$)'; then
    echo "BLOQUEADO: comando peligroso (rm -rf / push --force). Proponé una alternativa segura." >&2
    exit 2
  fi
fi

exit 0
