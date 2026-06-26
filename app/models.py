"""Modelos de datos.

NOTA: la columna de monto se llama `value`. (En una versión vieja del sistema
se llamaba `amount`; quedó algún módulo legacy sin actualizar...)
"""
from sqlalchemy import Column, Float, Integer, String

from app.db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, index=True)   # formato "YYYY-MM", ej "2026-01"
    category = Column(String)
    value = Column(Float)                 # monto de la transacción
