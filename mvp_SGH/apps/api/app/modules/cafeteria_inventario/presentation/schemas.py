from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class CrearProductoRequest(BaseModel):
    nombre: str
    precio: float = Field(ge=0)
    stock: int = Field(ge=0, default=0)
    categoria: str = "general"

class RegistrarConsumoRequest(BaseModel):
    estadia_id: UUID
    producto_id: UUID
    cantidad: int = Field(gt=0)

class ProductoResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    nombre: str
    precio: float
    stock: int
    categoria: str
    activo: bool
    created_at: datetime

class ConsumoResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    estadia_id: UUID
    producto_id: UUID
    cantidad: int
    precio_unitario: float
    total: float
    created_at: datetime
