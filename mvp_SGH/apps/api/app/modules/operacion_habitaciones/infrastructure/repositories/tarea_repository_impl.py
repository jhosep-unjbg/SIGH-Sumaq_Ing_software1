from typing import Dict, List, Optional
from uuid import UUID
from app.modules.operacion_habitaciones.domain.entities.tarea_limpieza import TareaLimpieza
from app.modules.operacion_habitaciones.domain.repositories.tarea_repository import ITareaRepository

_STORE: Dict[UUID, TareaLimpieza] = {}

class TareaRepositoryImpl(ITareaRepository):
    async def get_by_id(self, tarea_id, tenant_id):
        t = _STORE.get(tarea_id)
        return t if t and t.tenant_id == tenant_id else None
    async def list_by_tenant(self, tenant_id, skip=0, limit=50):
        return [t for t in _STORE.values() if t.tenant_id == tenant_id][skip:skip+limit]
    async def save(self, tarea):
        _STORE[tarea.id] = tarea
        return tarea
