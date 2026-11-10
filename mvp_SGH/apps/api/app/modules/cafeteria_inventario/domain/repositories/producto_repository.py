from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.modules.cafeteria_inventario.domain.entities.producto import Producto
from app.modules.cafeteria_inventario.domain.entities.consumo import Consumo

class IProductoRepository(ABC):
    @abstractmethod
    async def get_by_id(self, producto_id: UUID, tenant_id: UUID) -> Optional[Producto]: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: UUID) -> List[Producto]: ...
    @abstractmethod
    async def save(self, producto: Producto) -> Producto: ...
    @abstractmethod
    async def save_consumo(self, consumo: Consumo) -> Consumo: ...
    @abstractmethod
    async def list_consumos(self, tenant_id: UUID) -> List[Consumo]: ...
