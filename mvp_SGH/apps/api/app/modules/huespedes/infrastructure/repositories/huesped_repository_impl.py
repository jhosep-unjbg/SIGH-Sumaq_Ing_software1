from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.huespedes.domain.entities.huesped import Huesped
from app.modules.huespedes.domain.repositories.huesped_repository import IHuespedRepository
from app.modules.huespedes.infrastructure.persistence.models import HuespedModel


class HuespedRepositoryImpl(IHuespedRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(
        self,
        huesped_id: UUID,
        tenant_id: UUID,
    ) -> Optional[Huesped]:
        model = await self._session.scalar(
            select(HuespedModel).where(
                HuespedModel.id == huesped_id,
                HuespedModel.tenant_id == tenant_id,
            )
        )
        return self._to_entity(model) if model else None

    async def list_by_tenant(self, tenant_id: UUID) -> List[Huesped]:
        models = await self._session.scalars(
            select(HuespedModel)
            .where(HuespedModel.tenant_id == tenant_id)
            .order_by(HuespedModel.created_at, HuespedModel.id)
        )
        return [self._to_entity(model) for model in models]

    async def save(self, huesped: Huesped) -> Huesped:
        model = HuespedModel(
            id=huesped.id,
            tenant_id=huesped.tenant_id,
            nombre=huesped.nombre,
            activo=huesped.activo,
            created_at=huesped.created_at,
        )
        saved = await self._session.merge(model)
        await self._session.commit()
        await self._session.refresh(saved)
        return self._to_entity(saved)

    @staticmethod
    def _to_entity(model: HuespedModel) -> Huesped:
        return Huesped(
            id=model.id,
            tenant_id=model.tenant_id,
            nombre=model.nombre,
            activo=model.activo,
            created_at=model.created_at,
        )
