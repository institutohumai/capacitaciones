"""Lógica del endpoint de reportes."""
from sqlalchemy.orm import Session

from app.legacy_aggregator import aggregate_monthly
from app.models import Transaction


def monthly_report(db: Session) -> dict:
    """Devuelve {mes: total} a partir de las transacciones de la DB."""
    rows = db.query(Transaction).all()
    # Mapeamos a dicts con la columna actual ("value")
    txns = [{"month": r.month, "category": r.category, "value": r.value} for r in rows]
    return aggregate_monthly(txns)
