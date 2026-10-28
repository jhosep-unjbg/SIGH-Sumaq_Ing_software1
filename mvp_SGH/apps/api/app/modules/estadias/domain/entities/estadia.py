"""Entidad de dominio: Estadía"""
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class EstadoEstadia(str, Enum):
    RESERVADA = "reservada"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELADA = "cancelada"


@dataclass
class Estadia:
    id: UUID
    tenant_id: UUID
    reserva_id: UUID
    habitacion_id: UUID
    huesped_id: UUID
    fecha_entrada: date
    fecha_salida: date
    estado: EstadoEstadia
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    checked_in_at: Optional[datetime] = None
    checked_out_at: Optional[datetime] = None

    @staticmethod
    def crear(tenant_id, reserva_id, habitacion_id, huesped_id, fecha_entrada, fecha_salida):
        if fecha_salida <= fecha_entrada:
            raise ValueError("fecha_salida debe ser posterior a fecha_entrada")
        return Estadia(
            id=uuid4(), tenant_id=tenant_id, reserva_id=reserva_id,
            habitacion_id=habitacion_id, huesped_id=huesped_id,
            fecha_entrada=fecha_entrada, fecha_salida=fecha_salida,
            estado=EstadoEstadia.RESERVADA,
        )

    def check_in(self):
        if self.estado != EstadoEstadia.RESERVADA:
            raise ValueError(f"No se puede hacer check-in en estado {self.estado}")
        self.estado = EstadoEstadia.CHECKED_IN
        self.checked_in_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def check_out(self):
        if self.estado != EstadoEstadia.CHECKED_IN:
            raise ValueError(f"No se puede hacer check-out en estado {self.estado}")
        self.estado = EstadoEstadia.CHECKED_OUT
        self.checked_out_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
