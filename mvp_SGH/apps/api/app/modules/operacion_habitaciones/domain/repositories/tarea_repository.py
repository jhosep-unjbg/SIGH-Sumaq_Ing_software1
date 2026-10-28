from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.modules.operacion_habitaciones.domain.entities.tarea_limpieza import TareaLimpieza

class ITareaRepository(ABC):
    @abstractmethod
    async def get_by_id(self, tarea_id: UUID, tenant_id: UUID) -> Optional[TareaLimpieza]: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: UUID, skip: int = 0, limit: int = 50) -> List[TareaLimpieza]: ...
    @abstractmethod
    async def save(self, tarea: TareaLimpieza) -> TareaLimpieza: ...
