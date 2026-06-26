"""Carga datos de ejemplo en la DB (idempotente)."""
from app.db import Base, SessionLocal, engine
from app.models import Transaction

SAMPLE = [
    ("2026-01", "ventas", 100.0),
    ("2026-01", "ventas", 200.0),
    ("2026-02", "ventas", 150.0),
    ("2026-02", "servicios", 50.0),
    ("2026-03", "ventas", 300.0),
]

# Totales esperados: 2026-01 -> 300, 2026-02 -> 200, 2026-03 -> 300


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Transaction).count() == 0:
            for month, category, value in SAMPLE:
                db.add(Transaction(month=month, category=category, value=value))
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("DB sembrada.")
