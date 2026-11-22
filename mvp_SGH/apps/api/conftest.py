import os
from datetime import date
from typing import Dict, List, Optional
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://test:test@localhost:5432/test",
)

from app.main import app
from app.modules.huespedes.domain.entities.huesped import Huesped
from app.modules.huespedes.presentation.dependencies import (
    get_huesped_repository as get_huespedes_repository,
)
from app.modules.reservas.domain.entities.reserva import EstadoReserva, Reserva
from app.modules.reservas.presentation.dependencies import (
    get_huesped_repository as get_reserva_huesped_repository,
)
from app.modules.reservas.presentation.dependencies import (
    get_reserva_repository,
)


class FakeHuespedRepository:
    def __init__(self) -> None:
        self.huespedes: Dict[UUID, Huesped] = {}

    async def get_by_id(
        self,
        huesped_id: UUID,
        tenant_id: UUID,
    ) -> Optional[Huesped]:
        huesped = self.huespedes.get(huesped_id)
        if huesped and huesped.tenant_id == tenant_id:
            return huesped
        return None

    async def list_by_tenant(self, tenant_id: UUID) -> List[Huesped]:
        return [
            huesped
            for huesped in self.huespedes.values()
            if huesped.tenant_id == tenant_id
        ]

    async def save(self, huesped: Huesped) -> Huesped:
        self.huespedes[huesped.id] = huesped
        return huesped


class FakeReservaRepository:
    def __init__(self) -> None:
        self.reservas: Dict[UUID, Reserva] = {}

    async def get_by_id(self, reserva_id: UUID, tenant_id: UUID) -> Optional[Reserva]:
        reserva = self.reservas.get(reserva_id)
        if reserva and reserva.tenant_id == tenant_id:
            return reserva
        return None

    async def list_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Reserva]:
        reservas = [
            reserva
            for reserva in self.reservas.values()
            if reserva.tenant_id == tenant_id
        ]
        return reservas[skip : skip + limit]

    async def save(self, reserva: Reserva) -> Reserva:
        self.reservas[reserva.id] = reserva
        return reserva

    async def delete(self, reserva_id: UUID, tenant_id: UUID) -> None:
        reserva = self.reservas.get(reserva_id)
        if reserva and reserva.tenant_id == tenant_id:
            del self.reservas[reserva_id]

    async def existe_conflicto(
        self,
        tenant_id: UUID,
        habitacion_id: UUID,
        fecha_entrada: date,
        fecha_salida: date,
        excluir_reserva_id: Optional[UUID] = None,
    ) -> bool:
        estados_que_no_bloquean = {
            EstadoReserva.CANCELADA,
            EstadoReserva.CHECKED_OUT,
            EstadoReserva.NO_SHOW,
        }
        return any(
            reserva.tenant_id == tenant_id
            and reserva.habitacion_id == habitacion_id
            and reserva.id != excluir_reserva_id
            and reserva.estado not in estados_que_no_bloquean
            and reserva.fecha_entrada < fecha_salida
            and reserva.fecha_salida > fecha_entrada
            for reserva in self.reservas.values()
        )


@pytest.fixture
def client():
    huesped_repository = FakeHuespedRepository()
    reserva_repository = FakeReservaRepository()
    app.dependency_overrides[get_huespedes_repository] = lambda: huesped_repository
    app.dependency_overrides[get_reserva_huesped_repository] = (
        lambda: huesped_repository
    )
    app.dependency_overrides[get_reserva_repository] = lambda: reserva_repository

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
