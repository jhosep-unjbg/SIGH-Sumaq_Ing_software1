from uuid import UUID
from app.common.exceptions import DomainError
from app.modules.estadias.domain.entities.estadia import Estadia
from app.modules.estadias.domain.repositories.estadia_repository import IEstadiaRepository
from app.modules.estadias.application.dto.estadia_dto import CrearEstadiaDTO, EstadiaResponseDTO

class CrearEstadiaUseCase:
    def __init__(self, repo: IEstadiaRepository):
        self._repo = repo

    async def execute(self, dto: CrearEstadiaDTO, tenant_id: UUID) -> EstadiaResponseDTO:
        try:
            estadia = Estadia.crear(
                tenant_id=tenant_id, reserva_id=dto.reserva_id,
                habitacion_id=dto.habitacion_id, huesped_id=dto.huesped_id,
                fecha_entrada=dto.fecha_entrada, fecha_salida=dto.fecha_salida,
            )
        except ValueError as e:
            raise DomainError(str(e))
        saved = await self._repo.save(estadia)
        return EstadiaResponseDTO.from_entity(saved)
