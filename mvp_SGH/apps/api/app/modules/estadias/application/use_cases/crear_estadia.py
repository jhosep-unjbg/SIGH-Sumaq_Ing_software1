"""Caso de uso para crear una estadía."""

from uuid import UUID

from app.common.exceptions import DomainError
from app.modules.estadias.application.dto.estadia_dto import (
    CrearEstadiaDTO,
    EstadiaResponseDTO,
)
from app.modules.estadias.domain.entities.estadia import Estadia
from app.modules.estadias.domain.repositories.estadia_repository import (
    IEstadiaRepository,
)


class CrearEstadiaUseCase:
    """Crea y guarda una estadía."""

    def __init__(self, repo: IEstadiaRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        dto: CrearEstadiaDTO,
        tenant_id: UUID,
    ) -> EstadiaResponseDTO:
        """Crea una estadía a partir de los datos recibidos."""
        estadia = self._crear_entidad(dto, tenant_id)
        estadia_guardada = await self._repo.save(estadia)

        return EstadiaResponseDTO.from_entity(estadia_guardada)

    @staticmethod
    def _crear_entidad(dto: CrearEstadiaDTO, tenant_id: UUID) -> Estadia:
        try:
            return Estadia.crear(
                tenant_id=tenant_id,
                reserva_id=dto.reserva_id,
                habitacion_id=dto.habitacion_id,
                huesped_id=dto.huesped_id,
                fecha_entrada=dto.fecha_entrada,
                fecha_salida=dto.fecha_salida,
            )
        except ValueError as error:
            raise DomainError(str(error)) from error