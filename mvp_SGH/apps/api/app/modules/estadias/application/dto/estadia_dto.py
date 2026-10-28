from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.modules.estadias.domain.entities.estadia import Estadia, EstadoEstadia

class CrearEstadiaDTO(BaseModel):
    reserva_id: UUID
    habitacion_id: UUID
    huesped_id: UUID
    fecha_entrada: date
    fecha_salida: date

class EstadiaResponseDTO(BaseModel):
    id: UUID
    tenant_id: UUID
    reserva_id: UUID
    habitacion_id: UUID
    huesped_id: UUID
    fecha_entrada: date
    fecha_salida: date
    estado: EstadoEstadia
    checked_in_at: Optional[datetime]
    checked_out_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, e: Estadia):
        return cls(
            id=e.id, tenant_id=e.tenant_id, reserva_id=e.reserva_id,
            habitacion_id=e.habitacion_id, huesped_id=e.huesped_id,
            fecha_entrada=e.fecha_entrada, fecha_salida=e.fecha_salida,
            estado=e.estado, checked_in_at=e.checked_in_at,
            checked_out_at=e.checked_out_at, created_at=e.created_at,
            updated_at=e.updated_at,
        )
