from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.modules.identidad_acceso.domain.entities.usuario import Usuario

class IUsuarioRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID, tenant_id: UUID) -> Optional[Usuario]: ...
    @abstractmethod
    async def get_by_email(self, email: str, tenant_id: UUID) -> Optional[Usuario]: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: UUID) -> List[Usuario]: ...
    @abstractmethod
    async def save(self, usuario: Usuario) -> Usuario: ...
