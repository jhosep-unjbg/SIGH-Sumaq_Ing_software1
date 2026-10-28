from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class Consumo:
    id: UUID
    tenant_id: UUID
    estadia_id: UUID
    producto_id: UUID
    cantidad: int
    precio_unitario: float
    total: float
    created_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def crear(tenant_id, estadia_id, producto_id, cantidad, precio_unitario):
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        return Consumo(
            id=uuid4(), tenant_id=tenant_id, estadia_id=estadia_id,
            producto_id=producto_id, cantidad=cantidad,
            precio_unitario=precio_unitario, total=cantidad * precio_unitario,
        )
