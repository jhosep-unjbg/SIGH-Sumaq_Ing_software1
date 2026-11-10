from uuid import UUID
from app.common.exceptions import DomainError, NotFoundError
from app.modules.estadias.domain.repositories.estadia_repository import IEstadiaRepository
from app.modules.estadias.application.dto.estadia_dto import EstadiaResponseDTO

class CheckInUseCase:
    def __init__(self, repo: IEstadiaRepository):
        self._repo = repo

    async def execute(self, estadia_id: UUID, tenant_id: UUID) -> EstadiaResponseDTO:
        estadia = await self._repo.get_by_id(estadia_id, tenant_id)
        if not estadia:
            raise NotFoundError("Estadía no encontrada")
        try:
            estadia.check_in()
        except ValueError as e:
            raise DomainError(str(e))
        saved = await self._repo.save(estadia)
        return EstadiaResponseDTO.from_entity(saved)
