# Quantit Reports — repo de ejemplo (capacitación AI-Assisted Coding)

MVP mínimo y realista para los ejercicios de la capacitación: una API de
reportes mensuales (FastAPI + Postgres) con un front React, deployable a Railway
y operable con `gh` + `railway`.

> Repo: `institutohumai/capacitaciones`, rama `quantit-main`.
> Clonar: `git clone -b quantit-main https://github.com/institutohumai/capacitaciones.git`

> ⚠️ Este repo tiene **deuda técnica y un bug sembrados a propósito** para los
> ejercicios. No es código de producción.

## Stack

- **Backend**: FastAPI + SQLAlchemy. Corre con SQLite por defecto (sin docker) o
  Postgres vía `DATABASE_URL`.
- **Front**: React + Vite (`frontend/`).
- **Infra**: `docker-compose.yml` (API + Postgres), `Dockerfile`, `railway.json`.

## Levantar el proyecto

### Opción A — sólo backend, sin docker (rápido)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload      # http://localhost:8000
```

`GET /reports/monthly` → totales por mes. `GET /health` → healthcheck.

### Opción B — stack completo con docker

```bash
docker compose up -d               # API en :8000, Postgres en :5432
docker compose logs api | tail -n 100
```

### Front

```bash
cd frontend
npm install
npm run dev                        # http://localhost:5173
```

## Tests

```bash
python3 -m pytest -q
```

Vas a ver **1 test que falla** (`tests/test_integration.py`): los totales
mensuales dan 0. La causa real **sólo se ve en los logs** de la API. Ese es el
bug del ejercicio E4.

## Deploy a Railway

```bash
railway init
railway add --database postgres
railway up -d
railway logs
```

## Skills de ejemplo

En `skills-ejemplo/` hay un kit de skills sanitizadas, ancladas a este repo
(ver `skills-ejemplo/README.md`):

- `ops` — ejemplo real combinado: `gh` + `railway` (PRs, deploy, logs). → B4
- `cli-wrapper` — patrón para envolver cualquier CLI. → B4 ①
- `read-logs` — debuggear leyendo el error real en logs acotados. → B4 ②
- `db-explorer` — inspeccionar la base con queries de sólo lectura. → B4 ③
- `knowledge-base` — skill sin CLI, conocimiento del dominio. → B3

Para activar cualquiera:

```bash
mkdir -p .claude/skills && cp -r skills-ejemplo/<skill> .claude/skills/
```

## Deuda técnica sembrada (para los ejercicios)

- `app/legacy_aggregator.py`: módulo enredado (E2) + **bug visible sólo en logs** (E4).
- Una función inexistente (`normalize_band`) detrás de una rama muerta (AI smell).
- Un umbral mágico `THRESHOLD = 1000` sin justificar.
- Un test comentado en `tests/test_reports.py` (AI smell).
- No hay `CLAUDE.md`: lo crean en el ejercicio E1.
