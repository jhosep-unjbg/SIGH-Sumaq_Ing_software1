from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Huesped:
    id: UUID
    tenant_id: UUID
    nombre: str
    activo: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def crear(tenant_id: UUID, nombre: str) -> "Huesped":
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            raise ValueError("El nombre del huésped es obligatorio")

        return Huesped(
            id=uuid4(),
            tenant_id=tenant_id,
            nombre=nombre_limpio,
        )
