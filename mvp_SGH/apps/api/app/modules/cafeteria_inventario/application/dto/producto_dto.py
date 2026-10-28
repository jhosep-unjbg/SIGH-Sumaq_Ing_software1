from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.modules.cafeteria_inventario.domain.entities.producto import Producto
from app.modules.cafeteria_inventario.domain.entities.consumo import Consumo

class CrearProductoDTO(BaseModel):
    nombre: str
    precio: float = Field(ge=0)
    stock: int = Field(ge=0, default=0)
    categoria: str = "general"

class RegistrarConsumoDTO(BaseModel):
    estadia_id: UUID
    producto_id: UUID
    cantidad: int = Field(gt=0)

class ProductoResponseDTO(BaseModel):
    id: UUID
    tenant_id: UUID
    nombre: str
    precio: float
    stock: int
    categoria: str
    activo: bool
    created_at: datetime

    @classmethod
    def from_entity(cls, p: Producto):
        return cls(id=p.id, tenant_id=p.tenant_id, nombre=p.nombre, precio=p.precio,
                   stock=p.stock, categoria=p.categoria, activo=p.activo, created_at=p.created_at)

class ConsumoResponseDTO(BaseModel):
    id: UUID
    tenant_id: UUID
    estadia_id: UUID
    producto_id: UUID
    cantidad: int
    precio_unitario: float
    total: float
    created_at: datetime

    @classmethod
    def from_entity(cls, c: Consumo):
        return cls(id=c.id, tenant_id=c.tenant_id, estadia_id=c.estadia_id,
                   producto_id=c.producto_id, cantidad=c.cantidad,
                   precio_unitario=c.precio_unitario, total=c.total, created_at=c.created_at)
