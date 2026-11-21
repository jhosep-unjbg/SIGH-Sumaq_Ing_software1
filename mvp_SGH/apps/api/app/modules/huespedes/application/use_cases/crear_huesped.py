from uuid import UUID

from app.common.exceptions import DomainError
from app.modules.huespedes.application.dto.huesped_dto import (
    CrearHuespedDTO,
    HuespedResponseDTO,
)
from app.modules.huespedes.domain.entities.huesped import Huesped
from app.modules.huespedes.domain.repositories.huesped_repository import IHuespedRepository


class CrearHuespedUseCase:
    def __init__(self, huesped_repo: IHuespedRepository) -> None:
        self._huesped_repo = huesped_repo

    async def execute(
        self,
        dto: CrearHuespedDTO,
        tenant_id: UUID,
    ) -> HuespedResponseDTO:
        try:
            huesped = Huesped.crear(tenant_id=tenant_id, nombre=dto.nombre)
        except ValueError as error:
            raise DomainError(str(error)) from error

        guardado = await self._huesped_repo.save(huesped)
        return HuespedResponseDTO(
            id=guardado.id,
            tenant_id=guardado.tenant_id,
            nombre=guardado.nombre,
            activo=guardado.activo,
            created_at=guardado.created_at,
        )
