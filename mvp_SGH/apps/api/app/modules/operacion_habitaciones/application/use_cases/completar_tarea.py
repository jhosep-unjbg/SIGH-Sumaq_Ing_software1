"""Caso de uso para completar una tarea de limpieza."""

from uuid import UUID

from app.common.exceptions import DomainError, NotFoundError
from app.modules.operacion_habitaciones.application.dto.tarea_dto import (
    TareaResponseDTO,
)
from app.modules.operacion_habitaciones.domain.repositories.tarea_repository import (
    ITareaRepository,
)


class CompletarTareaUseCase:
    """Busca una tarea y marca su finalización."""

    def __init__(self, repo: ITareaRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        tarea_id: UUID,
        tenant_id: UUID,
    ) -> TareaResponseDTO:
        """Completa una tarea existente del hotel indicado."""
        tarea = await self._repo.get_by_id(tarea_id, tenant_id)
        if tarea is None:
            raise NotFoundError("Tarea no encontrada")

        try:
            tarea.completar()
        except ValueError as error:
            raise DomainError(str(error)) from error

        tarea_guardada = await self._repo.save(tarea)
        return TareaResponseDTO.from_entity(tarea_guardada)