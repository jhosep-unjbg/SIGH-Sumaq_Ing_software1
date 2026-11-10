from uuid import UUID
from app.common.exceptions import DomainError
from app.modules.cuentas_pagos.domain.entities.cargo import Cargo
from app.modules.cuentas_pagos.domain.repositories.cuenta_repository import ICuentaRepository
from app.modules.cuentas_pagos.application.dto.cuenta_dto import CrearCargoDTO, CargoResponseDTO

class CrearCargoUseCase:
    def __init__(self, repo: ICuentaRepository):
        self._repo = repo
    async def execute(self, dto: CrearCargoDTO, tenant_id: UUID) -> CargoResponseDTO:
        try:
            cargo = Cargo.crear(tenant_id, dto.estadia_id, dto.descripcion, dto.monto, dto.tipo)
        except ValueError as e:
            raise DomainError(str(e))
        saved = await self._repo.save_cargo(cargo)
        return CargoResponseDTO.from_entity(saved)
