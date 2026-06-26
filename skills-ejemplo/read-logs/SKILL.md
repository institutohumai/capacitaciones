---
name: read-logs
description: Debuggear leyendo logs acotados antes de proponer un fix. Usar cuando el usuario diga "no entiendo por qué falla", "los totales dan 0", "anda local pero no en prod", "fijate en los logs", o cuando un síntoma no se explica leyendo sólo el código. Lee el error real (no asume la causa), lo acota, y recién entonces propone el arreglo.
---

# Read Logs — debuggear leyendo el error real

> Plantilla de ejemplo (sanitizada) del kit de la capacitación. Para activarla:
> `mkdir -p .claude/skills && cp -r skills-ejemplo/read-logs .claude/skills/`

El error más caro es el que se *traga* y reaparece como un síntoma silencioso
(un total en 0, una lista vacía, un 200 que debería ser 500). El código puede
verse bien; la causa está en los logs. Esta skill fuerza el orden correcto:

> **Leer el error real → acotar → entender → recién ahí proponer el fix.**
> Nunca al revés. No asumir la causa por leer el código.

## 1. Conseguir los logs — siempre acotados

Pedí una ventana chica, no el stream completo (satura el contexto y esconde la
señal):

```bash
# Stack local con docker
docker compose logs api | tail -n 100
docker compose logs api --since 5m          # sólo lo reciente

# Sin docker (uvicorn en foreground): el log ya sale por stdout
uvicorn app.main:app --reload

# En Railway (prod)
railway logs | tail -n 100
railway logs --build                         # si el deploy ni arranca
```

Si buscás un síntoma concreto, filtrá:

```bash
docker compose logs api | grep -i error | tail -n 30
```

## 2. Leer el error real

Buscá el nivel `ERROR`/`WARNING` y la **primera** línea de la cadena (la causa,
no el síntoma de arrastre). Fijate en el `logger` que la emite: te dice qué módulo.

## 3. Recién entonces, el fix

Conectá la línea de log con el código que la emite. Cambiá lo mínimo. Volvé a
correr y confirmá que el log ofensivo desapareció.

## Ejemplo anclado a este repo — "los totales mensuales dan 0"

Síntoma: `GET /reports/monthly` devuelve todos los meses en `0.0`. El código de
`reports.py` se ve correcto. La causa **sólo aparece en los logs**:

```
2026-06-25 12:00:01 ERROR reports.aggregator | Failed to aggregate month 2026-01: 'amount'
```

Lectura: el `logger` es `reports.aggregator` → el problema está en
`app/legacy_aggregator.py`. El mensaje `'amount'` es un `KeyError`: ese módulo
legacy lee `tx["amount"]`, pero la columna real del modelo se llama `value`
(ver `app/models.py`). El `except Exception` se traga el error y deja el total en
0 — por eso no explota, sólo "da mal".

Fix: en `legacy_aggregator.py`, leer `tx["value"]` en vez de `tx["amount"]`.
Después: `pytest -q` queda verde y el log de ERROR desaparece.

> Este es el bug del ejercicio **E4**: el síntoma está en la API, la causa está
> en los logs, y el `except` que "loguea y sigue" es lo que lo vuelve invisible.

## Cómo adaptarla a tu stack

- Cambiá los comandos de la parte 1 por los de tu plataforma (`kubectl logs`,
  `journalctl -u <svc> -n 100`, `heroku logs --tail`, `aws logs tail`).
- Mantené la regla de oro: **acotar siempre** (`tail -n`, `--since`, `grep`).
- Mantené el orden: leer antes de teorizar. La trampa más común es proponer un
  fix plausible que no toca la causa real.
