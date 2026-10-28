from typing import Dict, List, Optional
from uuid import UUID
from app.modules.cuentas_pagos.domain.entities.cargo import Cargo, Pago
from app.modules.cuentas_pagos.domain.repositories.cuenta_repository import ICuentaRepository

_CARGOS: Dict[UUID, Cargo] = {}
_PAGOS: Dict[UUID, Pago] = {}

class CuentaRepositoryImpl(ICuentaRepository):
    async def save_cargo(self, cargo):
        _CARGOS[cargo.id] = cargo
        return cargo
    async def get_cargo(self, cargo_id, tenant_id):
        c = _CARGOS.get(cargo_id)
        return c if c and c.tenant_id == tenant_id else None
    async def list_cargos(self, tenant_id, estadia_id=None):
        items = [c for c in _CARGOS.values() if c.tenant_id == tenant_id]
        if estadia_id:
            items = [c for c in items if c.estadia_id == estadia_id]
        return items
    async def save_pago(self, pago):
        _PAGOS[pago.id] = pago
        return pago
    async def list_pagos(self, tenant_id, estadia_id=None):
        items = [p for p in _PAGOS.values() if p.tenant_id == tenant_id]
        if estadia_id:
            items = [p for p in items if p.estadia_id == estadia_id]
        return items
