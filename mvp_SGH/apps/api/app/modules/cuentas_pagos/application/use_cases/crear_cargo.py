"""Caso de uso para crear un cargo de estadía."""

from uuid import UUID

from app.common.exceptions import DomainError
from app.modules.cuentas_pagos.application.dto.cuenta_dto import (
    CargoResponseDTO,
    CrearCargoDTO,
)
from app.modules.cuentas_pagos.domain.entities.cargo import Cargo
from app.modules.cuentas_pagos.domain.repositories.cuenta_repository import (
    ICuentaRepository,
)


class CrearCargoUseCase:
    """Crea y guarda un cargo asociado a una estadía."""

    def __init__(self, repo: ICuentaRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        dto: CrearCargoDTO,
        tenant_id: UUID,
    ) -> CargoResponseDTO:
        """Crea un cargo con los datos recibidos."""
        try:
            cargo = Cargo.crear(
                tenant_id=tenant_id,
                estadia_id=dto.estadia_id,
                descripcion=dto.descripcion,
                monto=dto.monto,
                tipo=dto.tipo,
            )
        except ValueError as error:
            raise DomainError(str(error)) from error

        cargo_guardado = await self._repo.save_cargo(cargo)
        return CargoResponseDTO.from_entity(cargo_guardado)