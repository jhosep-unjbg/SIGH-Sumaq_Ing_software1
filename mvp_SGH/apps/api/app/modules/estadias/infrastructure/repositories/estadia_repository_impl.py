from typing import Dict, List, Optional
from uuid import UUID
from app.modules.estadias.domain.entities.estadia import Estadia
from app.modules.estadias.domain.repositories.estadia_repository import IEstadiaRepository

_STORE: Dict[UUID, Estadia] = {}

class EstadiaRepositoryImpl(IEstadiaRepository):
    async def get_by_id(self, estadia_id, tenant_id):
        e = _STORE.get(estadia_id)
        return e if e and e.tenant_id == tenant_id else None

    async def list_by_tenant(self, tenant_id, skip=0, limit=50):
        items = [e for e in _STORE.values() if e.tenant_id == tenant_id]
        return items[skip:skip+limit]

    async def save(self, estadia):
        _STORE[estadia.id] = estadia
        return estadia
