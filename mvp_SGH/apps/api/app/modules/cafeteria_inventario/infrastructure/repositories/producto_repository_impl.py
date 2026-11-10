from typing import Dict, List, Optional
from uuid import UUID
from app.modules.cafeteria_inventario.domain.entities.producto import Producto
from app.modules.cafeteria_inventario.domain.entities.consumo import Consumo
from app.modules.cafeteria_inventario.domain.repositories.producto_repository import IProductoRepository

_PRODUCTOS: Dict[UUID, Producto] = {}
_CONSUMOS: Dict[UUID, Consumo] = {}

class ProductoRepositoryImpl(IProductoRepository):
    async def get_by_id(self, producto_id, tenant_id):
        p = _PRODUCTOS.get(producto_id)
        return p if p and p.tenant_id == tenant_id else None
    async def list_by_tenant(self, tenant_id):
        return [p for p in _PRODUCTOS.values() if p.tenant_id == tenant_id]
    async def save(self, producto):
        _PRODUCTOS[producto.id] = producto
        return producto
    async def save_consumo(self, consumo):
        _CONSUMOS[consumo.id] = consumo
        return consumo
    async def list_consumos(self, tenant_id):
        return [c for c in _CONSUMOS.values() if c.tenant_id == tenant_id]
