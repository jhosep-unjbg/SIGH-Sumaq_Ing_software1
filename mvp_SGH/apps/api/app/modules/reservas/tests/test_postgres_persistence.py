import asyncio
import os
from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.modules.huespedes.domain.entities.huesped import Huesped
from app.modules.huespedes.infrastructure.persistence.models import HuespedModel
from app.modules.huespedes.infrastructure.repositories.huesped_repository_impl import (
    HuespedRepositoryImpl,
)
from app.modules.reservas.domain.entities.reserva import EstadoReserva, Reserva
from app.modules.reservas.infrastructure.persistence.models import ReservaModel
from app.modules.reservas.infrastructure.repositories.reserva_repository_impl import (
    ReservaRepositoryImpl,
)


@pytest.mark.skipif(
    not os.environ.get("TEST_DATABASE_URL"),
    reason="Set TEST_DATABASE_URL to run PostgreSQL persistence integration test",
)
def test_guest_and_reservation_survive_new_database_session():
    asyncio.run(_verify_persistence(os.environ["TEST_DATABASE_URL"]))


async def _verify_persistence(database_url: str) -> None:
    tenant_id = uuid4()
    guest = Huesped.crear(tenant_id=tenant_id, nombre="Persistencia M2")
    reservation = Reserva.crear(
        tenant_id=tenant_id,
        habitacion_id=uuid4(),
        huesped_id=guest.id,
        fecha_entrada=date(2035, 5, 10),
        fecha_salida=date(2035, 5, 12),
        precio_total=250.0,
    )
    engine = create_async_engine(database_url, pool_pre_ping=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with session_factory() as session:
            await HuespedRepositoryImpl(session).save(guest)
            await ReservaRepositoryImpl(session).save(reservation)

        async with session_factory() as session:
            persisted_guest = await HuespedRepositoryImpl(session).get_by_id(
                guest.id,
                tenant_id,
            )
            persisted_reservation = await ReservaRepositoryImpl(session).get_by_id(
                reservation.id,
                tenant_id,
            )

        assert persisted_guest is not None
        assert persisted_guest.nombre == guest.nombre
        assert persisted_reservation is not None
        assert persisted_reservation.id == reservation.id
        assert persisted_reservation.estado is EstadoReserva.PENDIENTE
    finally:
        async with session_factory() as session:
            await session.execute(
                delete(ReservaModel).where(ReservaModel.tenant_id == tenant_id)
            )
            await session.execute(
                delete(HuespedModel).where(HuespedModel.tenant_id == tenant_id)
            )
            await session.commit()
        await engine.dispose()
