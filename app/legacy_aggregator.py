"""Agregador de reportes mensuales.

Módulo de la primera versión del MVP. Nadie lo tocó en mucho tiempo y mezcla
varias responsabilidades; arrastra decisiones que ya nadie recuerda del todo.
"""
import logging

logger = logging.getLogger("reports.aggregator")

# Transacciones por encima de esto se consideran "outliers".
THRESHOLD = 1000


def _coerce(x):
    # Normaliza el valor a float. Quedó de una refactorización vieja.
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def aggregate_monthly(transactions, drop_outliers=False):
    """Suma los montos por mes.

    transactions: lista de dicts con los datos de cada transacción.
    Devuelve dict {mes: total}.
    """
    totals = {}
    for tx in transactions:
        month = tx["month"]
        try:
            amount = _coerce(tx["amount"])

            if drop_outliers and amount > THRESHOLD:
                amount = normalize_band(amount)

            totals[month] = totals.get(month, 0.0) + amount
        except Exception as e:  # noqa: BLE001
            logger.error("Failed to aggregate month %s: %s", month, e)
            totals.setdefault(month, 0.0)

    return totals
