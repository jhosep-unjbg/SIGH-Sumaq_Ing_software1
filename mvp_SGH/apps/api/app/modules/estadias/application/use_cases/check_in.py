"""Caso de uso para registrar el check-in de una estadía."""

from uuid import UUID

from app.common.exceptions import DomainError, NotFoundError
from app.modules.estadias.application.dto.estadia_dto import EstadiaResponseDTO
from app.modules.estadias.domain.repositories.estadia_repository import (
    IEstadiaRepository,
)


class CheckInUseCase:
    """Busca una estadía y registra su check-in."""

    def __init__(self, repo: IEstadiaRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        estadia_id: UUID,
        tenant_id: UUID,
    ) -> EstadiaResponseDTO:
        """Registra el check-in si la estadía existe y permite el cambio."""
        estadia = await self._repo.get_by_id(estadia_id, tenant_id)
        if estadia is None:
            raise NotFoundError("Estadía no encontrada")

        try:
            estadia.check_in()
        except ValueError as error:
            raise DomainError(str(error)) from error

        estadia_guardada = await self._repo.save(estadia)
        return EstadiaResponseDTO.from_entity(estadia_guardada)