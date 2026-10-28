from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.modules.identidad_acceso.domain.entities.usuario import Usuario, Rol

class CrearUsuarioDTO(BaseModel):
    email: str
    nombre: str
    rol: Rol = Rol.RECEPCION
    password: str = "changeme"

class LoginDTO(BaseModel):
    email: str
    password: str

class UsuarioResponseDTO(BaseModel):
    id: UUID
    tenant_id: UUID
    email: str
    nombre: str
    rol: Rol
    activo: bool
    created_at: datetime

    @classmethod
    def from_entity(cls, u: Usuario):
        return cls(id=u.id, tenant_id=u.tenant_id, email=u.email, nombre=u.nombre,
                   rol=u.rol, activo=u.activo, created_at=u.created_at)

class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponseDTO
