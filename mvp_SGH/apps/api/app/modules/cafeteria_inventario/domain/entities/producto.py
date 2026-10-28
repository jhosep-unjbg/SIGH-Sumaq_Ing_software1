from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class Producto:
    id: UUID
    tenant_id: UUID
    nombre: str
    precio: float
    stock: int
    categoria: str = "general"
    activo: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def crear(tenant_id, nombre, precio, stock=0, categoria="general"):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        return Producto(id=uuid4(), tenant_id=tenant_id, nombre=nombre,
                        precio=precio, stock=stock, categoria=categoria)

    def descontar_stock(self, cantidad: int):
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        if self.stock < cantidad:
            raise ValueError(f"Stock insuficiente: disponible={self.stock}")
        self.stock -= cantidad
