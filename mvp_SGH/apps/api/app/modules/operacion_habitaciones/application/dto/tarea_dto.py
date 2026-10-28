from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.modules.operacion_habitaciones.domain.entities.tarea_limpieza import TareaLimpieza, EstadoTarea

class CrearTareaDTO(BaseModel):
    habitacion_id: UUID
    asignado_a: Optional[UUID] = None
    notas: Optional[str] = None

class TareaResponseDTO(BaseModel):
    id: UUID
    tenant_id: UUID
    habitacion_id: UUID
    asignado_a: Optional[UUID]
    estado: EstadoTarea
    notas: Optional[str]
    created_at: datetime
    updated_at: datetime
    completada_at: Optional[datetime]

    @classmethod
    def from_entity(cls, t: TareaLimpieza):
        return cls(
            id=t.id, tenant_id=t.tenant_id, habitacion_id=t.habitacion_id,
            asignado_a=t.asignado_a, estado=t.estado, notas=t.notas,
            created_at=t.created_at, updated_at=t.updated_at, completada_at=t.completada_at,
        )
