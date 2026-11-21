from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.modules.huespedes.domain.entities.huesped import Huesped


class IHuespedRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        huesped_id: UUID,
        tenant_id: UUID,
    ) -> Optional[Huesped]:
        ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: UUID) -> List[Huesped]:
        ...

    @abstractmethod
    async def save(self, huesped: Huesped) -> Huesped:
        ...
