---
name: knowledge-base
description: Conocimiento del dominio del proyecto Quantit Reports — glosario, convenciones, mapa de la arquitectura y trampas conocidas. Usar cuando alguien (o Claude) necesite entender "cómo funciona este proyecto", qué significa un término del negocio, dónde vive cada cosa, o por qué algo está hecho de cierta forma. Es una skill de conocimiento (sin CLI): no ejecuta nada, aporta contexto curado bajo demanda.
---

# Knowledge Base — el dominio de Quantit Reports

> Plantilla de ejemplo (sanitizada) del kit de la capacitación. Para activarla:
> `mkdir -p .claude/skills && cp -r skills-ejemplo/knowledge-base .claude/skills/`

No todas las skills envuelven un CLI. Una **skill de conocimiento** no ejecuta
comandos: empaqueta el entendimiento del dominio que normalmente vive sólo en la
cabeza de la gente senior. Claude la consulta cuando la necesita y deja de
adivinar convenciones del negocio.

> **¿Skill de conocimiento o `CLAUDE.md`?**
> `CLAUDE.md` es memoria *siempre activa* y breve (reglas que aplican a casi todo).
> Una skill de conocimiento es *bajo demanda* y puede ser más rica y larga: se
> carga sólo cuando el tema aparece (progressive disclosure). Regla práctica: lo
> que aplica siempre → `CLAUDE.md`; el cuerpo de conocimiento de un sub-dominio →
> skill. Las dos se complementan; no compiten.

## Glosario del dominio

| Término            | Qué es en este proyecto                                            |
|--------------------|-------------------------------------------------------------------|
| **Transacción**    | Una fila de `transactions`: un movimiento con mes, categoría y monto. |
| **`month`**        | String `YYYY-MM` (ej. `2026-01`). No es fecha completa: es el bucket mensual. |
| **`value`**        | El **monto** de la transacción. ⚠️ Antes se llamaba `amount` (ver trampas). |
| **`category`**     | Etiqueta libre de la transacción.                                 |
| **Reporte mensual**| `GET /reports/monthly` → `{mes: total}`, sumando `value` por `month`. |
| **Outlier**        | Transacción por encima de `THRESHOLD` (1000). Hoy no se filtra (rama muerta). |

## Mapa de la arquitectura (dónde vive cada cosa)

```
app/
  main.py              # FastAPI: /health, /reports/monthly, CORS, logging, seed on startup
  models.py            # modelo Transaction(id, month, category, value)
  db.py                # engine SQLAlchemy; DATABASE_URL (SQLite por defecto / Postgres)
  reports.py           # arma los dicts y delega en el agregador
  legacy_aggregator.py # suma por mes — módulo legacy, acá vive la deuda y el bug
  seed.py              # datos de ejemplo al arrancar
frontend/              # React + Vite, consume /reports/monthly
```

## Convenciones

- La columna de monto es **`value`** en todo lo nuevo. `amount` es un nombre
  histórico que NO debe usarse (sólo sobrevive en el módulo legacy, y es un bug).
- Los meses son strings `YYYY-MM`, no `datetime`. Comparar y agrupar como string.
- Logs con formato `asctime LEVEL logger | mensaje`; el `logger` identifica el módulo.
- Salida de logs y queries **siempre acotada** (ver skills `read-logs` y `db-explorer`).

## Trampas conocidas (deuda sembrada a propósito)

- **Bug `amount`/`value`** — `legacy_aggregator.py` lee `tx["amount"]`; la columna
  real es `value`. El `except Exception` se traga el `KeyError` → los totales dan
  0 y sólo se ve en los logs. (Ejercicio E4.)
- **`normalize_band(...)`** — función inexistente detrás de una rama muerta
  (`drop_outliers` nunca llega en `True` desde la API). Alucinación latente: no la
  "completes", está muerta.
- **`THRESHOLD = 1000`** — umbral mágico sin justificar. Si hay que tocarlo,
  primero documentar de dónde sale.
- **Test comentado** en `tests/test_reports.py` — AI smell; no lo borres sin
  entender por qué se comentó.

## Cómo adaptarla a tu proyecto

- Reemplazá glosario, mapa y convenciones por los de tu dominio. Apuntá a lo que
  un dev nuevo (o Claude) pregunta el primer día y nadie tiene escrito.
- Si el cuerpo crece, partilo: dejá lo esencial en `SKILL.md` y mové el detalle a
  `references/` (ej. `references/glosario.md`, `references/arquitectura.md`), que
  Claude lee sólo cuando hace falta. Eso es progressive disclosure.
- Mantené la skill *descriptiva*, no *ejecutable*: si querés que además corra algo,
  esa parte va en una skill-CLI aparte (ver `cli-wrapper`).
