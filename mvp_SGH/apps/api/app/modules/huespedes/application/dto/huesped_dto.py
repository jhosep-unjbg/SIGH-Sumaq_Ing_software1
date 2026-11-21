from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class CrearHuespedDTO:
    nombre: str


@dataclass(frozen=True)
class HuespedResponseDTO:
    id: UUID
    tenant_id: UUID
    nombre: str
    activo: bool
    created_at: datetime
