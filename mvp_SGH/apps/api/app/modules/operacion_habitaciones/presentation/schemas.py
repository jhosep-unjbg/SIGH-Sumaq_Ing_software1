from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class CrearTareaRequest(BaseModel):
    habitacion_id: UUID
    asignado_a: Optional[UUID] = None
    notas: Optional[str] = None

class TareaResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    habitacion_id: UUID
    asignado_a: Optional[UUID]
    estado: str
    notas: Optional[str]
    created_at: datetime
    updated_at: datetime
    completada_at: Optional[datetime]
