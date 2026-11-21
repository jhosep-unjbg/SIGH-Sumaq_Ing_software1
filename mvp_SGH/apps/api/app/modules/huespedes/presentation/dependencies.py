from fastapi import Depends

from app.modules.huespedes.application.use_cases.crear_huesped import CrearHuespedUseCase
from app.modules.huespedes.domain.repositories.huesped_repository import IHuespedRepository
from app.modules.huespedes.infrastructure.repositories.huesped_repository_impl import (
    HuespedRepositoryImpl,
)


def get_huesped_repository() -> IHuespedRepository:
    return HuespedRepositoryImpl()


def get_crear_huesped_use_case(
    repo: IHuespedRepository = Depends(get_huesped_repository),
) -> CrearHuespedUseCase:
    return CrearHuespedUseCase(huesped_repo=repo)
