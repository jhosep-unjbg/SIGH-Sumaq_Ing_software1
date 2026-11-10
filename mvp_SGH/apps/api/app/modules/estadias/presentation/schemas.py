from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class CrearEstadiaRequest(BaseModel):
    reserva_id: UUID
    habitacion_id: UUID
    huesped_id: UUID
    fecha_entrada: date
    fecha_salida: date

class EstadiaResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    reserva_id: UUID
    habitacion_id: UUID
    huesped_id: UUID
    fecha_entrada: date
    fecha_salida: date
    estado: str
    checked_in_at: Optional[datetime]
    checked_out_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
