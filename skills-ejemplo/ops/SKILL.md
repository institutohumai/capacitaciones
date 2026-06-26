---
name: ops
description: Operar el proyecto Quantit Reports — abrir PRs con gh, deployar a Railway y leer logs del servicio. Usar cuando el usuario pida "abrir un PR", "deployar", "subir a Railway", "ver los logs de prod", o diagnosticar un problema del servicio deployado.
---

# Ops — GitHub + Railway

> Skill de ejemplo (sanitizada). Para activarla, copiala a `.claude/skills/ops/`
> en el repo:  `mkdir -p .claude/skills && cp -r skills-ejemplo/ops .claude/skills/`

Envuelve los CLIs `gh` y `railway` para encapsular el flujo del proyecto. El CLI
sigue siendo la fuente de verdad; esto sólo le da a Claude una superficie
agent-native y las convenciones del equipo.

> Los secretos NUNCA van acá. Se leen de `.env` / variables de entorno o del
> login ya hecho (`gh auth login`, `railway login`).

## Antes de cualquier operación

```bash
gh auth status          # verificar sesión de GitHub
railway whoami          # verificar sesión de Railway
```

## Abrir un PR

```bash
git checkout -b <rama>
git add -A && git commit -m "<mensaje>"
git push -u origin <rama>
gh pr create --fill --base main
```

Usar el template del repo (`.github/pull_request_template.md`) y completar el checklist.

## Deploy a Railway

```bash
railway up -d            # deploy en background
railway logs            # ver logs del deploy (deploy logs por defecto)
railway logs --build    # ver logs del build si el deploy falla
```

## Leer logs para debuggear

Pedir SIEMPRE logs acotados, no el stream completo:

```bash
railway logs | tail -n 100
# local equivalente:
docker compose logs api | tail -n 100
```

Leer el error real antes de proponer un fix. No asumir la causa.

## Equivalencias (otras nubes, para referencia)

| Tarea     | Railway          | GCP                    | AWS                  |
|-----------|------------------|------------------------|----------------------|
| Deploy    | `railway up`     | `gcloud run deploy`    | `copilot deploy`     |
| Ver logs  | `railway logs`   | `gcloud logging read`  | `aws logs tail`      |
