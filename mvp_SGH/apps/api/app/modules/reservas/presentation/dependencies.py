"""
Inyección de dependencias del módulo de Reservas - MVP
"""

from fastapi import Depends

from app.modules.reservas.application.use_cases.crear_reserva import CrearReservaUseCase
from app.modules.reservas.domain.repositories.reserva_repository import IReservaRepository
from app.modules.reservas.infrastructure.repositories.reserva_repository_impl import (
    ReservaRepositoryImpl,
)


def get_reserva_repository() -> IReservaRepository:
    return ReservaRepositoryImpl()


def get_crear_reserva_use_case(
    repo: IReservaRepository = Depends(get_reserva_repository),
) -> CrearReservaUseCase:
    return CrearReservaUseCase(reserva_repo=repo)
