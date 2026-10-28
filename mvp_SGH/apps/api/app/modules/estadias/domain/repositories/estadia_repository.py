from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.modules.estadias.domain.entities.estadia import Estadia

class IEstadiaRepository(ABC):
    @abstractmethod
    async def get_by_id(self, estadia_id: UUID, tenant_id: UUID) -> Optional[Estadia]: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: UUID, skip: int = 0, limit: int = 50) -> List[Estadia]: ...
    @abstractmethod
    async def save(self, estadia: Estadia) -> Estadia: ...
