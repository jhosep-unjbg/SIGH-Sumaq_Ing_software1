"""Caso de uso para consultar el saldo de una estadía."""

from uuid import UUID

from app.modules.cuentas_pagos.application.dto.cuenta_dto import SaldoResponseDTO
from app.modules.cuentas_pagos.domain.repositories.cuenta_repository import (
    ICuentaRepository,
)


class ConsultarSaldoUseCase:
    """Calcula el saldo a partir de cargos y pagos registrados."""

    _ESTADO_CARGO_ANULADO = "anulado"

    def __init__(self, repo: ICuentaRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        estadia_id: UUID,
        tenant_id: UUID,
    ) -> SaldoResponseDTO:
        """Devuelve cargos, pagos y saldo de la estadía."""
        cargos = await self._repo.list_cargos(tenant_id, estadia_id)
        pagos = await self._repo.list_pagos(tenant_id, estadia_id)

        total_cargos = sum(
            cargo.monto
            for cargo in cargos
            if cargo.estado.value != self._ESTADO_CARGO_ANULADO
        )
        total_pagos = sum(pago.monto for pago in pagos)

        return SaldoResponseDTO(
            estadia_id=estadia_id,
            total_cargos=total_cargos,
            total_pagos=total_pagos,
            saldo=total_cargos - total_pagos,
        )