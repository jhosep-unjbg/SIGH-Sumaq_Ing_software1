from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.reservas.domain.entities.reserva import EstadoReserva, Reserva
from app.modules.reservas.domain.repositories.reserva_repository import IReservaRepository
from app.modules.reservas.infrastructure.persistence.models import ReservaModel


class ReservaRepositoryImpl(IReservaRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, reserva_id: UUID, tenant_id: UUID) -> Optional[Reserva]:
        model = await self._session.scalar(
            select(ReservaModel).where(
                ReservaModel.id == reserva_id,
                ReservaModel.tenant_id == tenant_id,
            )
        )
        return self._to_entity(model) if model else None

    async def list_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Reserva]:
        models = await self._session.scalars(
            select(ReservaModel)
            .where(ReservaModel.tenant_id == tenant_id)
            .order_by(ReservaModel.created_at, ReservaModel.id)
            .offset(skip)
            .limit(limit)
        )
        return [self._to_entity(model) for model in models]

    async def save(self, reserva: Reserva) -> Reserva:
        model = ReservaModel(
            id=reserva.id,
            tenant_id=reserva.tenant_id,
            habitacion_id=reserva.habitacion_id,
            huesped_id=reserva.huesped_id,
            fecha_entrada=reserva.fecha_entrada,
            fecha_salida=reserva.fecha_salida,
            estado=reserva.estado.value,
            precio_total=reserva.precio_total,
            moneda=reserva.moneda,
            notas=reserva.notas,
            created_at=reserva.created_at,
            updated_at=reserva.updated_at,
        )
        saved = await self._session.merge(model)
        await self._session.commit()
        await self._session.refresh(saved)
        return self._to_entity(saved)

    async def delete(self, reserva_id: UUID, tenant_id: UUID) -> None:
        await self._session.execute(
            delete(ReservaModel).where(
                ReservaModel.id == reserva_id,
                ReservaModel.tenant_id == tenant_id,
            )
        )
        await self._session.commit()

    async def existe_conflicto(
        self,
        tenant_id: UUID,
        habitacion_id: UUID,
        fecha_entrada: date,
        fecha_salida: date,
        excluir_reserva_id: Optional[UUID] = None,
    ) -> bool:
        conditions = [
            ReservaModel.tenant_id == tenant_id,
            ReservaModel.habitacion_id == habitacion_id,
            ReservaModel.fecha_entrada < fecha_salida,
            ReservaModel.fecha_salida > fecha_entrada,
            ~ReservaModel.estado.in_(
                [
                    EstadoReserva.CANCELADA.value,
                    EstadoReserva.CHECKED_OUT.value,
                    EstadoReserva.NO_SHOW.value,
                ]
            ),
        ]
        if excluir_reserva_id is not None:
            conditions.append(ReservaModel.id != excluir_reserva_id)

        statement = select(exists().where(*conditions))
        return bool(await self._session.scalar(statement))

    @staticmethod
    def _to_entity(model: ReservaModel) -> Reserva:
        return Reserva(
            id=model.id,
            tenant_id=model.tenant_id,
            habitacion_id=model.habitacion_id,
            huesped_id=model.huesped_id,
            fecha_entrada=model.fecha_entrada,
            fecha_salida=model.fecha_salida,
            estado=EstadoReserva(model.estado),
            precio_total=float(model.precio_total),
            moneda=model.moneda,
            notas=model.notas,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
