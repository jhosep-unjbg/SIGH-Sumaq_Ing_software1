from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class CrearUsuarioRequest(BaseModel):
    email: str
    nombre: str
    rol: str = "recepcion"
    password: str = "changeme"

class LoginRequest(BaseModel):
    email: str
    password: str

class UsuarioResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    email: str
    nombre: str
    rol: str
    activo: bool
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse
