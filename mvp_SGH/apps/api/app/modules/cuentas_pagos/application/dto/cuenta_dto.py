from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.modules.cuentas_pagos.domain.entities.cargo import Cargo, Pago, TipoCargo, EstadoPago

class CrearCargoDTO(BaseModel):
    estadia_id: UUID
    descripcion: str
    monto: float = Field(gt=0)
    tipo: TipoCargo = TipoCargo.OTRO

class RegistrarPagoDTO(BaseModel):
    estadia_id: UUID
    monto: float = Field(gt=0)
    metodo: str = "efectivo"
    referencia: Optional[str] = None

class CargoResponseDTO(BaseModel):
    id: UUID
    tenant_id: UUID
    estadia_id: UUID
    descripcion: str
    monto: float
    tipo: TipoCargo
    estado: EstadoPago
    created_at: datetime

    @classmethod
    def from_entity(cls, c: Cargo):
        return cls(id=c.id, tenant_id=c.tenant_id, estadia_id=c.estadia_id,
                   descripcion=c.descripcion, monto=c.monto, tipo=c.tipo,
                   estado=c.estado, created_at=c.created_at)

class PagoResponseDTO(BaseModel):
    id: UUID
    tenant_id: UUID
    estadia_id: UUID
    monto: float
    metodo: str
    referencia: Optional[str]
    created_at: datetime

    @classmethod
    def from_entity(cls, p: Pago):
        return cls(id=p.id, tenant_id=p.tenant_id, estadia_id=p.estadia_id,
                   monto=p.monto, metodo=p.metodo, referencia=p.referencia,
                   created_at=p.created_at)

class SaldoResponseDTO(BaseModel):
    estadia_id: UUID
    total_cargos: float
    total_pagos: float
    saldo: float
