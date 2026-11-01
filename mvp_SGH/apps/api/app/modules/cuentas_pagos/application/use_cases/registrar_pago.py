"""Caso de uso para registrar un pago."""

from uuid import UUID

from app.common.exceptions import DomainError
from app.modules.cuentas_pagos.application.dto.cuenta_dto import (
    PagoResponseDTO,
    RegistrarPagoDTO,
)
from app.modules.cuentas_pagos.domain.entities.cargo import Pago
from app.modules.cuentas_pagos.domain.repositories.cuenta_repository import (
    ICuentaRepository,
)


class RegistrarPagoUseCase:
    """Crea y guarda un pago asociado a una estadía."""

    def __init__(self, repo: ICuentaRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        dto: RegistrarPagoDTO,
        tenant_id: UUID,
    ) -> PagoResponseDTO:
        """Registra un pago con los datos recibidos."""
        try:
            pago = Pago.crear(
                tenant_id=tenant_id,
                estadia_id=dto.estadia_id,
                monto=dto.monto,
                metodo=dto.metodo,
                referencia=dto.referencia,
            )
        except ValueError as error:
            raise DomainError(str(error)) from error

        pago_guardado = await self._repo.save_pago(pago)
        return PagoResponseDTO.from_entity(pago_guardado)