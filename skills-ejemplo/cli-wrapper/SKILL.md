---
name: cli-wrapper
description: Envolver un CLI (gh, railway, docker, aws, gcloud…) como skill para que Claude lo opere con las convenciones del equipo. Usar cuando el usuario quiera "convertir este CLI en skill", "que Claude maneje gh/railway", automatizar un flujo de línea de comandos, o estandarizar cómo se invoca una herramienta. El CLI sigue siendo la fuente de verdad; la skill sólo le da a Claude una superficie agent-native y las reglas del equipo.
---

# CLI Wrapper — patrón para envolver una herramienta de línea de comandos

> Plantilla de ejemplo (sanitizada) del kit de la capacitación. Para activarla,
> copiala a `.claude/skills/` en el repo:
> `mkdir -p .claude/skills && cp -r skills-ejemplo/cli-wrapper .claude/skills/`

Una skill que envuelve un CLI **no reimplementa** la herramienta: la documenta para
Claude. El valor es triple:

1. **Convenciones del equipo** — qué flags usamos, qué subcomandos preferimos,
   en qué orden, con qué nombres de rama/entorno.
2. **Barandas de seguridad** — qué *no* hacer (nunca `--force`, nunca borrar
   recursos prod, salida siempre acotada).
3. **Superficie estable** — Claude no tiene que adivinar la sintaxis cada vez ni
   reinventar el flujo; lee la skill y opera igual que un humano del equipo.

> Los secretos NUNCA van en la skill. Se leen del login ya hecho (`gh auth login`,
> `railway login`) o de variables de entorno / `.env`.

## La receta (4 partes)

Toda skill que envuelve un CLI tiene la misma estructura. Copiá este esqueleto y
rellenalo para tu herramienta:

1. **Verificar sesión antes de operar** — fallar temprano y claro si no hay login.
2. **Comandos canónicos** — el subconjunto que el equipo realmente usa, con sus flags.
3. **Salida acotada** — nunca volcar streams infinitos; `tail`/`--limit`/`-n`.
4. **Equivalencias** (opcional) — el mismo flujo en otra nube, para referencia.

## Ejemplo anclado a este repo — `gh` + `railway`

### 1. Verificar sesión

```bash
gh auth status          # sesión de GitHub
railway whoami          # sesión de Railway
```

Si alguno falla, pará y pedile al usuario que haga `gh auth login` /
`railway login`. No intentes adivinar credenciales.

### 2. Comandos canónicos

```bash
# Abrir un PR (usa el template del repo y completa el checklist)
git checkout -b <rama>
git add -A && git commit -m "<mensaje>"
git push -u origin <rama>
gh pr create --fill --base main

# Deploy a Railway
railway up -d           # deploy en background
railway status          # estado del servicio
```

### 3. Salida acotada

```bash
railway logs | tail -n 100
gh run list --limit 10
```

### 4. Equivalencias (otras nubes, para referencia)

| Tarea     | Railway          | GCP                    | AWS                  |
|-----------|------------------|------------------------|----------------------|
| Deploy    | `railway up`     | `gcloud run deploy`    | `copilot deploy`     |
| Ver logs  | `railway logs`   | `gcloud logging read`  | `aws logs tail`      |

## Barandas (importante)

- **Nunca** `git push --force` ni `--force-with-lease` sobre `main`.
- **Nunca** borrar recursos de un entorno prod (`railway down`, `gh repo delete`).
- Antes de un `deploy`, confirmar la rama y el entorno destino.
- Si un comando pide confirmación interactiva, mostrá el comando y pedí luz verde
  en vez de auto-confirmar a ciegas.

## Cómo adaptarla a tu CLI

Cambiá `gh`/`railway` por tu herramienta (`docker`, `kubectl`, `aws`, `stripe`,
`supabase`…) y volvé a llenar las 4 partes:

- ¿Cómo se verifica que hay sesión? → parte 1
- ¿Cuáles son los 4-6 comandos que tu equipo realmente corre? → parte 2
- ¿Cómo se acota la salida (logs, listas largas)? → parte 3
- ¿Qué operaciones son irreversibles y necesitan baranda? → "Barandas"

> Relación con la skill `ops`: `ops` es el ejemplo "real" ya combinado (gh +
> railway juntos para el flujo de este proyecto). `cli-wrapper` es la **plantilla
> reusable** que enseña el patrón para cualquier CLI.
