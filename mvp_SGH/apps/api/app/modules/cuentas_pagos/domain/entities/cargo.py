from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

class TipoCargo(str, Enum):
    HABITACION = "habitacion"
    CONSUMO = "consumo"
    SERVICIO = "servicio"
    OTRO = "otro"

class EstadoPago(str, Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    ANULADO = "anulado"

@dataclass
class Cargo:
    id: UUID
    tenant_id: UUID
    estadia_id: UUID
    descripcion: str
    monto: float
    tipo: TipoCargo
    estado: EstadoPago
    created_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def crear(tenant_id, estadia_id, descripcion, monto, tipo=TipoCargo.OTRO):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        return Cargo(id=uuid4(), tenant_id=tenant_id, estadia_id=estadia_id,
                     descripcion=descripcion, monto=monto, tipo=tipo, estado=EstadoPago.PENDIENTE)

    def marcar_pagado(self):
        if self.estado != EstadoPago.PENDIENTE:
            raise ValueError(f"No se puede pagar un cargo en estado {self.estado}")
        self.estado = EstadoPago.PAGADO

@dataclass
class Pago:
    id: UUID
    tenant_id: UUID
    estadia_id: UUID
    monto: float
    metodo: str
    referencia: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def crear(tenant_id, estadia_id, monto, metodo, referencia=None):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        return Pago(id=uuid4(), tenant_id=tenant_id, estadia_id=estadia_id,
                    monto=monto, metodo=metodo, referencia=referencia)
