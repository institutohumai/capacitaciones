"""
Agregador de reportes mensuales.

Este módulo viene arrastrándose desde la primera versión del MVP. Nadie lo tocó
en mucho tiempo y mezcla varias responsabilidades. Acumula deuda técnica:
nombres poco claros, una rama muerta, un umbral mágico sin justificar y un
manejo de errores que esconde problemas reales.

>>> Para la capacitación: este es el módulo que el subagente debe EXPLICAR (E2)
>>> y donde vive el BUG que sólo se ve en los logs (E4).
"""
import logging

logger = logging.getLogger("reports.aggregator")

# Umbral mágico: transacciones por encima de esto se consideran "outliers".
# (nadie documentó de dónde salió este número)
THRESHOLD = 1000


def _coerce(x):
    # helper viejo, medio inútil, quedó de una refactorización a medias
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def aggregate_monthly(transactions, drop_outliers=False):
    """Suma los montos por mes.

    transactions: lista de dicts con keys "month" y "value".
    Devuelve dict {mes: total}.
    """
    totals = {}
    for tx in transactions:
        month = tx["month"]
        try:
            # BUG: la columna real se llama "value", pero este código viejo
            # todavía lee "amount" (nombre anterior). Lanza KeyError y el
            # except de abajo lo esconde -> el total queda en 0.
            amount = _coerce(tx["amount"])

            if drop_outliers and amount > THRESHOLD:
                # rama muerta: drop_outliers nunca se pasa como True desde la API
                amount = normalize_band(amount)  # función inexistente (alucinación latente)

            totals[month] = totals.get(month, 0.0) + amount
        except Exception as e:  # noqa: BLE001 - traga todo y sólo loguea
            logger.error("Failed to aggregate month %s: %s", month, e)
            totals.setdefault(month, 0.0)

    return totals
