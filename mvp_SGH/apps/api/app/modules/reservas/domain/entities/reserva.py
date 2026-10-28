"""
Entidad de dominio: Reserva
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class EstadoReserva(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    NO_SHOW = "no_show"


@dataclass
class Reserva:
    """Agregado raíz del Bounded Context de Reservas."""

    id: UUID
    tenant_id: UUID
    habitacion_id: UUID
    huesped_id: UUID
    fecha_entrada: date
    fecha_salida: date
    estado: EstadoReserva
    precio_total: float
    moneda: str = "PEN"
    notas: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def crear(
        tenant_id: UUID,
        habitacion_id: UUID,
        huesped_id: UUID,
        fecha_entrada: date,
        fecha_salida: date,
        precio_total: float,
        moneda: str = "PEN",
        notas: Optional[str] = None,
    ) -> "Reserva":
        if fecha_salida <= fecha_entrada:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de entrada")
        if precio_total < 0:
            raise ValueError("El precio total no puede ser negativo")

        return Reserva(
            id=uuid4(),
            tenant_id=tenant_id,
            habitacion_id=habitacion_id,
            huesped_id=huesped_id,
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            estado=EstadoReserva.PENDIENTE,
            precio_total=precio_total,
            moneda=moneda,
            notas=notas,
        )

    def confirmar(self) -> None:
        if self.estado != EstadoReserva.PENDIENTE:
            raise ValueError(f"No se puede confirmar una reserva en estado {self.estado}")
        self.estado = EstadoReserva.CONFIRMADA
        self.updated_at = datetime.utcnow()

    def cancelar(self) -> None:
        if self.estado in (EstadoReserva.CANCELADA, EstadoReserva.CHECKED_OUT):
            raise ValueError(f"No se puede cancelar una reserva en estado {self.estado}")
        self.estado = EstadoReserva.CANCELADA
        self.updated_at = datetime.utcnow()

    def marcar_check_in(self) -> None:
        if self.estado != EstadoReserva.CONFIRMADA:
            raise ValueError("Solo se puede hacer check-in de una reserva confirmada")
        self.estado = EstadoReserva.CHECKED_IN
        self.updated_at = datetime.utcnow()
