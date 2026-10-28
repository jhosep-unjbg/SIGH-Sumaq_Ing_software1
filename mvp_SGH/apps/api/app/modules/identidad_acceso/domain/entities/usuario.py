from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

class Rol(str, Enum):
    ADMIN = "admin"
    RECEPCION = "recepcion"
    CAJERO = "cajero"
    LIMPIEZA = "limpieza"
    HUESPED = "huesped"

@dataclass
class Usuario:
    id: UUID
    tenant_id: UUID
    email: str
    nombre: str
    rol: Rol
    activo: bool = True
    password_hash: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def crear(tenant_id, email, nombre, rol, password_hash=""):
        return Usuario(id=uuid4(), tenant_id=tenant_id, email=email,
                       nombre=nombre, rol=rol, password_hash=password_hash)
