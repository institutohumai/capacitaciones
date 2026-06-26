"""Configuración de tests: DB SQLite temporal y datos sembrados."""
import os
import tempfile

import pytest

# Forzar SQLite temporal ANTES de importar la app
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp.name}"

from fastapi.testclient import TestClient  # noqa: E402

from app.db import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Transaction  # noqa: E402

SAMPLE = [
    ("2026-01", "ventas", 100.0),
    ("2026-01", "ventas", 200.0),
    ("2026-02", "ventas", 150.0),
    ("2026-02", "servicios", 50.0),
    ("2026-03", "ventas", 300.0),
]


@pytest.fixture(scope="session", autouse=True)
def _db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    for month, category, value in SAMPLE:
        db.add(Transaction(month=month, category=category, value=value))
    db.commit()
    db.close()
    yield


@pytest.fixture()
def client():
    return TestClient(app)
