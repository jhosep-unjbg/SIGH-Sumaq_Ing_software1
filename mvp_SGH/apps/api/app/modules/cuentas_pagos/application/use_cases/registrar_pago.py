from uuid import UUID
from app.common.exceptions import DomainError
from app.modules.cuentas_pagos.domain.entities.cargo import Pago
from app.modules.cuentas_pagos.domain.repositories.cuenta_repository import ICuentaRepository
from app.modules.cuentas_pagos.application.dto.cuenta_dto import RegistrarPagoDTO, PagoResponseDTO

class RegistrarPagoUseCase:
    def __init__(self, repo: ICuentaRepository):
        self._repo = repo
    async def execute(self, dto: RegistrarPagoDTO, tenant_id: UUID) -> PagoResponseDTO:
        try:
            pago = Pago.crear(tenant_id, dto.estadia_id, dto.monto, dto.metodo, dto.referencia)
        except ValueError as e:
            raise DomainError(str(e))
        saved = await self._repo.save_pago(pago)
        return PagoResponseDTO.from_entity(saved)
