from uuid import UUID
from app.modules.operacion_habitaciones.domain.entities.tarea_limpieza import TareaLimpieza
from app.modules.operacion_habitaciones.domain.repositories.tarea_repository import ITareaRepository
from app.modules.operacion_habitaciones.application.dto.tarea_dto import CrearTareaDTO, TareaResponseDTO

class CrearTareaUseCase:
    def __init__(self, repo: ITareaRepository):
        self._repo = repo
    async def execute(self, dto: CrearTareaDTO, tenant_id: UUID) -> TareaResponseDTO:
        tarea = TareaLimpieza.crear(tenant_id, dto.habitacion_id, dto.asignado_a, dto.notas)
        saved = await self._repo.save(tarea)
        return TareaResponseDTO.from_entity(saved)
