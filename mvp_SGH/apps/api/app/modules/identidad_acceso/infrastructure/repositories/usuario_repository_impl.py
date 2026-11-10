from typing import Dict, List, Optional
from uuid import UUID
from app.modules.identidad_acceso.domain.entities.usuario import Usuario
from app.modules.identidad_acceso.domain.repositories.usuario_repository import IUsuarioRepository

_STORE: Dict[UUID, Usuario] = {}

class UsuarioRepositoryImpl(IUsuarioRepository):
    async def get_by_id(self, user_id, tenant_id):
        u = _STORE.get(user_id)
        return u if u and u.tenant_id == tenant_id else None
    async def get_by_email(self, email, tenant_id):
        for u in _STORE.values():
            if u.email == email and u.tenant_id == tenant_id:
                return u
        return None
    async def list_by_tenant(self, tenant_id):
        return [u for u in _STORE.values() if u.tenant_id == tenant_id]
    async def save(self, usuario):
        _STORE[usuario.id] = usuario
        return usuario
