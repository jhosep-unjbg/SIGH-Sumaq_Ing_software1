"""Caso de uso para crear una tarea de limpieza."""

from uuid import UUID

from app.modules.operacion_habitaciones.application.dto.tarea_dto import (
    CrearTareaDTO,
    TareaResponseDTO,
)
from app.modules.operacion_habitaciones.domain.entities.tarea_limpieza import (
    TareaLimpieza,
)
from app.modules.operacion_habitaciones.domain.repositories.tarea_repository import (
    ITareaRepository,
)


class CrearTareaUseCase:
    """Crea y guarda una tarea de limpieza."""

    def __init__(self, repo: ITareaRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        dto: CrearTareaDTO,
        tenant_id: UUID,
    ) -> TareaResponseDTO:
        """Crea una tarea para la habitación indicada."""
        tarea = TareaLimpieza.crear(
            tenant_id=tenant_id,
            habitacion_id=dto.habitacion_id,
            asignado_a=dto.asignado_a,
            notas=dto.notas,
        )
        tarea_guardada = await self._repo.save(tarea)

        return TareaResponseDTO.from_entity(tarea_guardada)