from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db_session
from app.modules.huespedes.application.use_cases.crear_huesped import CrearHuespedUseCase
from app.modules.huespedes.domain.repositories.huesped_repository import IHuespedRepository
from app.modules.huespedes.infrastructure.repositories.huesped_repository_impl import (
    HuespedRepositoryImpl,
)


def get_huesped_repository(
    session: AsyncSession = Depends(get_db_session),
) -> IHuespedRepository:
    return HuespedRepositoryImpl(session)


def get_crear_huesped_use_case(
    repo: IHuespedRepository = Depends(get_huesped_repository),
) -> CrearHuespedUseCase:
    return CrearHuespedUseCase(huesped_repo=repo)
