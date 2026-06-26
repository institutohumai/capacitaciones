# Skills de ejemplo — kit de la capacitación

Plantillas de skills **sanitizadas** (sin secretos) y **ancladas a este repo**
(FastAPI + Postgres + `gh`/`railway`). Sirven como ejemplo para los bloques B3 y
B4 y como punto de partida para que cada equipo arme las suyas.

> Son **ejemplos para leer y adaptar**, no skills activas. Para activar una,
> copiala a `.claude/skills/` del repo:
> `mkdir -p .claude/skills && cp -r skills-ejemplo/<skill> .claude/skills/`
>
> Los secretos nunca van en una skill: se leen del login ya hecho o de `.env`.

## El kit

| Skill            | Qué enseña                                              | Bloque |
|------------------|---------------------------------------------------------|--------|
| `ops`            | Ejemplo "real" combinado: `gh` + `railway` para el flujo del proyecto (PRs, deploy, logs) | B4 |
| `cli-wrapper`    | El **patrón** para envolver cualquier CLI como skill (las 4 partes + barandas) | B4 ① |
| `read-logs`      | Debuggear **leyendo el error real** en logs acotados (el bug de E4) | B4 ② |
| `db-explorer`    | Inspeccionar la base con queries de **sólo lectura**    | B4 ③ |
| `knowledge-base` | Skill **sin CLI**: conocimiento del dominio (vs. `CLAUDE.md`) | B3 |

`ops` es el ejemplo ya combinado; `cli-wrapper`, `read-logs` y `db-explorer` son
la versión granular (una responsabilidad cada una) que se presenta en B4 para
mostrar cada mecanismo limpio. `knowledge-base` es el contraste: una skill que no
ejecuta nada, sólo aporta contexto.

## Cómo se conectan con el repo

Las tres skills operativas giran alrededor del bug sembrado en
`app/legacy_aggregator.py` (lee `amount`, la columna real es `value`):

- **`read-logs`** encuentra la causa en los logs (`KeyError 'amount'`).
- **`db-explorer`** confirma desde los datos que la columna es `value` y no existe `amount`.
- **`cli-wrapper`** / **`ops`** abren el PR con el fix y lo deployan.
- **`knowledge-base`** documenta el dominio (incluida esa trampa) para que no
  vuelva a pasar.
