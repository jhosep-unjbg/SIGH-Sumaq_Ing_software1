from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

class EstadoTarea(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"

@dataclass
class TareaLimpieza:
    id: UUID
    tenant_id: UUID
    habitacion_id: UUID
    asignado_a: Optional[UUID]
    estado: EstadoTarea
    notas: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    completada_at: Optional[datetime] = None

    @staticmethod
    def crear(tenant_id, habitacion_id, asignado_a=None, notas=None):
        return TareaLimpieza(
            id=uuid4(), tenant_id=tenant_id, habitacion_id=habitacion_id,
            asignado_a=asignado_a, estado=EstadoTarea.PENDIENTE, notas=notas,
        )

    def iniciar(self):
        if self.estado != EstadoTarea.PENDIENTE:
            raise ValueError(f"No se puede iniciar en estado {self.estado}")
        self.estado = EstadoTarea.EN_PROGRESO
        self.updated_at = datetime.utcnow()

    def completar(self):
        if self.estado not in (EstadoTarea.PENDIENTE, EstadoTarea.EN_PROGRESO):
            raise ValueError(f"No se puede completar en estado {self.estado}")
        self.estado = EstadoTarea.COMPLETADA
        self.completada_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
