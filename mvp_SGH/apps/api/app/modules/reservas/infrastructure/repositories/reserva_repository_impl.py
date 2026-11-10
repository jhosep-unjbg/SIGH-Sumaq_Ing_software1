"""
Implementación en memoria del repositorio de Reservas (MVP).
En producción se reemplaza por SQLAlchemy + PostgreSQL.
"""

from datetime import date
from typing import Dict, List, Optional
from uuid import UUID

from app.modules.reservas.domain.entities.reserva import Reserva
from app.modules.reservas.domain.repositories.reserva_repository import IReservaRepository


# Store compartido en memoria para el MVP (simula base de datos)
_STORE: Dict[UUID, Reserva] = {}


class ReservaRepositoryImpl(IReservaRepository):

    async def get_by_id(self, reserva_id: UUID, tenant_id: UUID) -> Optional[Reserva]:
        reserva = _STORE.get(reserva_id)
        if reserva and reserva.tenant_id == tenant_id:
            return reserva
        return None

    async def list_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Reserva]:
        items = [r for r in _STORE.values() if r.tenant_id == tenant_id]
        return items[skip : skip + limit]

    async def save(self, reserva: Reserva) -> Reserva:
        _STORE[reserva.id] = reserva
        return reserva

    async def delete(self, reserva_id: UUID, tenant_id: UUID) -> None:
        reserva = await self.get_by_id(reserva_id, tenant_id)
        if reserva:
            del _STORE[reserva_id]

    async def existe_conflicto(
        self,
        tenant_id: UUID,
        habitacion_id: UUID,
        fecha_entrada: date,
        fecha_salida: date,
        excluir_reserva_id: Optional[UUID] = None,
    ) -> bool:
        for r in _STORE.values():
            if r.tenant_id != tenant_id:
                continue
            if r.habitacion_id != habitacion_id:
                continue
            if excluir_reserva_id and r.id == excluir_reserva_id:
                continue
            if r.estado.value in ("cancelada", "checked_out", "no_show"):
                continue
            # Solapamiento de fechas
            if fecha_entrada < r.fecha_salida and r.fecha_entrada < fecha_salida:
                return True
        return False
