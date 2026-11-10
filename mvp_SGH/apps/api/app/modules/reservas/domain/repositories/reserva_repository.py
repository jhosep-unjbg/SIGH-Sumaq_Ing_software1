"""
Contrato del repositorio de Reservas (sin SQL).
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from app.modules.reservas.domain.entities.reserva import Reserva


class IReservaRepository(ABC):

    @abstractmethod
    async def get_by_id(self, reserva_id: UUID, tenant_id: UUID) -> Optional[Reserva]:
        ...

    @abstractmethod
    async def list_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Reserva]:
        ...

    @abstractmethod
    async def save(self, reserva: Reserva) -> Reserva:
        ...

    @abstractmethod
    async def delete(self, reserva_id: UUID, tenant_id: UUID) -> None:
        ...

    @abstractmethod
    async def existe_conflicto(
        self,
        tenant_id: UUID,
        habitacion_id: UUID,
        fecha_entrada: date,
        fecha_salida: date,
        excluir_reserva_id: Optional[UUID] = None,
    ) -> bool:
        """Verifica si ya existe una reserva que solape el rango de fechas."""
        ...
