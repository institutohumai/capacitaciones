"""API de reportes — MVP de ejemplo para la capacitación.

Endpoints:
  GET /health            -> healthcheck
  GET /reports/monthly   -> totales por mes
"""
import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db import get_db
from app.reports import monthly_report
from app.seed import seed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s | %(message)s",
)

app = FastAPI(title="Quantit Reports Demo")

# Front local (Vite) en :5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    seed()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/reports/monthly")
def reports_monthly(db: Session = Depends(get_db)):
    return monthly_report(db)
