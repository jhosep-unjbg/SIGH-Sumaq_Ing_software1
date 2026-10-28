from uuid import UUID
from app.modules.cuentas_pagos.domain.repositories.cuenta_repository import ICuentaRepository
from app.modules.cuentas_pagos.application.dto.cuenta_dto import SaldoResponseDTO

class ConsultarSaldoUseCase:
    def __init__(self, repo: ICuentaRepository):
        self._repo = repo
    async def execute(self, estadia_id: UUID, tenant_id: UUID) -> SaldoResponseDTO:
        cargos = await self._repo.list_cargos(tenant_id, estadia_id)
        pagos = await self._repo.list_pagos(tenant_id, estadia_id)
        total_cargos = sum(c.monto for c in cargos if c.estado.value != "anulado")
        total_pagos = sum(p.monto for p in pagos)
        return SaldoResponseDTO(
            estadia_id=estadia_id,
            total_cargos=total_cargos,
            total_pagos=total_pagos,
            saldo=total_cargos - total_pagos,
        )
