from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class CrearCargoRequest(BaseModel):
    estadia_id: UUID
    descripcion: str
    monto: float = Field(gt=0)
    tipo: str = "otro"

class RegistrarPagoRequest(BaseModel):
    estadia_id: UUID
    monto: float = Field(gt=0)
    metodo: str = "efectivo"
    referencia: Optional[str] = None

class CargoResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    estadia_id: UUID
    descripcion: str
    monto: float
    tipo: str
    estado: str
    created_at: datetime

class PagoResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    estadia_id: UUID
    monto: float
    metodo: str
    referencia: Optional[str]
    created_at: datetime

class SaldoResponse(BaseModel):
    estadia_id: UUID
    total_cargos: float
    total_pagos: float
    saldo: float
