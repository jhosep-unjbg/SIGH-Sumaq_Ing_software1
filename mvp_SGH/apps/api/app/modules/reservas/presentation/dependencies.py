"""
Inyección de dependencias del módulo de Reservas - MVP
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db_session
from app.modules.huespedes.domain.repositories.huesped_repository import IHuespedRepository
from app.modules.huespedes.infrastructure.repositories.huesped_repository_impl import (
    HuespedRepositoryImpl,
)
from app.modules.reservas.application.use_cases.crear_reserva import CrearReservaUseCase
from app.modules.reservas.domain.repositories.reserva_repository import IReservaRepository
from app.modules.reservas.infrastructure.repositories.reserva_repository_impl import (
    ReservaRepositoryImpl,
)


def get_reserva_repository(
    session: AsyncSession = Depends(get_db_session),
) -> IReservaRepository:
    return ReservaRepositoryImpl(session)


def get_huesped_repository(
    session: AsyncSession = Depends(get_db_session),
) -> IHuespedRepository:
    return HuespedRepositoryImpl(session)


def get_crear_reserva_use_case(
    repo: IReservaRepository = Depends(get_reserva_repository),
    huesped_repo: IHuespedRepository = Depends(get_huesped_repository),
) -> CrearReservaUseCase:
    return CrearReservaUseCase(reserva_repo=repo, huesped_repo=huesped_repo)
