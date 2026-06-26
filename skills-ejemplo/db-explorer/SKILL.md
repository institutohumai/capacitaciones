---
name: db-explorer
description: Conectarse a la base de datos del proyecto y correr queries de SÓLO LECTURA para inspeccionar el esquema y los datos. Usar cuando el usuario pida "fijate qué hay en la base", "qué columnas tiene la tabla X", "cuántas filas", "verificá los datos", o cuando entender un bug requiera mirar la DB y no sólo el código. Nunca escribe ni borra: sólo SELECT / inspección de esquema.
---

# DB Explorer — inspeccionar la base, sin tocarla

> Plantilla de ejemplo (sanitizada) del kit de la capacitación. Para activarla:
> `mkdir -p .claude/skills && cp -r skills-ejemplo/db-explorer .claude/skills/`

Muchos bugs se entienden mirando los datos reales, no el código. Esta skill le da
a Claude una forma segura de **leer** la base: ver el esquema, contar filas,
mirar muestras. La regla es absoluta:

> **SÓLO LECTURA.** `SELECT`, `\d`, `.schema`, `COUNT`, `LIMIT`. Nunca `INSERT`,
> `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`. Si hace falta escribir, eso lo
> decide y ejecuta una persona, no la skill.

> La URL de conexión se lee de `DATABASE_URL` (o `.env`). Nunca se hardcodea ni se
> imprime con credenciales.

## 1. Saber a qué base te conectás

```bash
echo "$DATABASE_URL"     # ej: postgresql://...  ó  sqlite:///./reports.db
```

- Sin docker, este repo usa **SQLite** (`reports.db`) por defecto.
- Con `docker compose` o Railway, es **Postgres** (`DATABASE_URL` inyectada).

## 2. Inspeccionar el esquema (siempre primero)

**Postgres** (`psql "$DATABASE_URL"`):

```sql
\dt                      -- listar tablas
\d transactions          -- columnas y tipos de la tabla
```

**SQLite** (`sqlite3 reports.db`):

```sql
.tables
.schema transactions
```

## 3. Queries de lectura típicas

```sql
SELECT COUNT(*) FROM transactions;                       -- ¿cuántas filas?
SELECT * FROM transactions LIMIT 5;                      -- muestra
SELECT month, SUM(value) AS total                        -- el reporte, a mano
FROM transactions GROUP BY month ORDER BY month;
```

## Ejemplo anclado a este repo — confirmar el esquema real

El modelo (`app/models.py`) define la tabla `transactions` con las columnas:

| columna    | tipo    | nota                                  |
|------------|---------|---------------------------------------|
| `id`       | int     | PK                                    |
| `month`    | text    | formato `YYYY-MM`, ej `2026-01`       |
| `category` | text    | categoría de la transacción           |
| `value`    | float   | **el monto** (antes se llamaba `amount`) |

Inspeccionar el esquema confirma que la columna se llama `value` y que **no
existe `amount`**. Eso corrobora, desde los datos, el bug del agregador legacy
(que lee `tx["amount"]`) — el mismo que aparece en los logs del ejercicio E4. Y
el `SUM(value) GROUP BY month` te da el total correcto contra el cual comparar lo
que devuelve la API.

## Cómo adaptarla a tu proyecto

- Cambiá el cliente según tu motor: `psql` (Postgres), `sqlite3` (SQLite),
  `mysql` (MySQL), `mongosh` (Mongo).
- Documentá las 2-3 tablas centrales de tu dominio (como la tabla de arriba) para
  que Claude no tenga que descubrir el esquema cada vez.
- Mantené la baranda de **sólo lectura**. Si querés que sea imposible escribir,
  conectá con un rol de DB de sólo lectura y dejalo anotado acá.
