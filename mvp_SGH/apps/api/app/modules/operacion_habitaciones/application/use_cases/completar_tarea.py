from uuid import UUID
from app.common.exceptions import DomainError, NotFoundError
from app.modules.operacion_habitaciones.domain.repositories.tarea_repository import ITareaRepository
from app.modules.operacion_habitaciones.application.dto.tarea_dto import TareaResponseDTO

class CompletarTareaUseCase:
    def __init__(self, repo: ITareaRepository):
        self._repo = repo
    async def execute(self, tarea_id: UUID, tenant_id: UUID) -> TareaResponseDTO:
        tarea = await self._repo.get_by_id(tarea_id, tenant_id)
        if not tarea:
            raise NotFoundError("Tarea no encontrada")
        try:
            tarea.completar()
        except ValueError as e:
            raise DomainError(str(e))
        saved = await self._repo.save(tarea)
        return TareaResponseDTO.from_entity(saved)
