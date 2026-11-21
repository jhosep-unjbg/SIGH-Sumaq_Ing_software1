from typing import Dict, List, Optional
from uuid import UUID

from app.modules.huespedes.domain.entities.huesped import Huesped
from app.modules.huespedes.domain.repositories.huesped_repository import IHuespedRepository


_HUESPEDES: Dict[UUID, Huesped] = {}


class HuespedRepositoryImpl(IHuespedRepository):
    async def get_by_id(
        self,
        huesped_id: UUID,
        tenant_id: UUID,
    ) -> Optional[Huesped]:
        huesped = _HUESPEDES.get(huesped_id)
        if huesped and huesped.tenant_id == tenant_id:
            return huesped
        return None

    async def list_by_tenant(self, tenant_id: UUID) -> List[Huesped]:
        return [huesped for huesped in _HUESPEDES.values() if huesped.tenant_id == tenant_id]

    async def save(self, huesped: Huesped) -> Huesped:
        _HUESPEDES[huesped.id] = huesped
        return huesped
