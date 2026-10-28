"""
DTOs del módulo de Reservas
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.reservas.domain.entities.reserva import Reserva, EstadoReserva


class CrearReservaDTO(BaseModel):
    habitacion_id: UUID
    huesped_id: UUID
    fecha_entrada: date
    fecha_salida: date
    precio_total: float = Field(ge=0)
    moneda: str = "PEN"
    notas: Optional[str] = None


class ReservaResponseDTO(BaseModel):
    id: UUID
    tenant_id: UUID
    habitacion_id: UUID
    huesped_id: UUID
    fecha_entrada: date
    fecha_salida: date
    estado: EstadoReserva
    precio_total: float
    moneda: str
    notas: Optional[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, reserva: Reserva) -> "ReservaResponseDTO":
        return cls(
            id=reserva.id,
            tenant_id=reserva.tenant_id,
            habitacion_id=reserva.habitacion_id,
            huesped_id=reserva.huesped_id,
            fecha_entrada=reserva.fecha_entrada,
            fecha_salida=reserva.fecha_salida,
            estado=reserva.estado,
            precio_total=reserva.precio_total,
            moneda=reserva.moneda,
            notas=reserva.notas,
            created_at=reserva.created_at,
            updated_at=reserva.updated_at,
        )
