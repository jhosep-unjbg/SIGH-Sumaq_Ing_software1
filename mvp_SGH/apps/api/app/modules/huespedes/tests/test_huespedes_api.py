from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.huespedes.infrastructure.repositories.huesped_repository_impl import (
    _HUESPEDES,
)
from app.modules.reservas.infrastructure.repositories.reserva_repository_impl import _STORE


@pytest.fixture
def client():
    _HUESPEDES.clear()
    _STORE.clear()
    with TestClient(app) as test_client:
        yield test_client
    _HUESPEDES.clear()
    _STORE.clear()


def crear_huesped(client, tenant_id):
    return client.post(
        "/api/v1/huespedes/",
        headers={"X-Tenant-ID": str(tenant_id)},
        json={"nombre": "Huésped de prueba"},
    )


def payload_reserva(huesped_id):
    return {
        "habitacion_id": str(uuid4()),
        "huesped_id": str(huesped_id),
        "fecha_entrada": "2030-12-01",
        "fecha_salida": "2030-12-05",
        "precio_total": 800,
        "moneda": "PEN",
        "notas": "Prueba de integración",
    }


def test_registrar_y_listar_huesped_del_tenant(client):
    tenant_id = uuid4()
    creado = crear_huesped(client, tenant_id)

    assert creado.status_code == 201
    assert creado.json()["tenant_id"] == str(tenant_id)
    assert creado.json()["activo"] is True

    listado = client.get(
        "/api/v1/huespedes/",
        headers={"X-Tenant-ID": str(tenant_id)},
    )
    assert listado.status_code == 200
    assert len(listado.json()) == 1
    assert listado.json()[0]["id"] == creado.json()["id"]


def test_listar_huespedes_no_expone_datos_de_otros_tenants(client):
    tenant_id = uuid4()
    otro_tenant_id = uuid4()
    creado = crear_huesped(client, tenant_id)

    listado = client.get(
        "/api/v1/huespedes/",
        headers={"X-Tenant-ID": str(otro_tenant_id)},
    )

    assert creado.status_code == 201
    assert listado.status_code == 200
    assert listado.json() == []


def test_reserva_acepta_huesped_registrado_en_el_mismo_tenant(client):
    tenant_id = uuid4()
    huesped = crear_huesped(client, tenant_id)

    respuesta = client.post(
        "/api/v1/reservas/",
        headers={"X-Tenant-ID": str(tenant_id)},
        json=payload_reserva(huesped.json()["id"]),
    )

    assert huesped.status_code == 201
    assert respuesta.status_code == 201
    assert respuesta.json()["huesped_id"] == huesped.json()["id"]


def test_reserva_rechaza_huesped_inexistente(client):
    respuesta = client.post(
        "/api/v1/reservas/",
        headers={"X-Tenant-ID": str(uuid4())},
        json=payload_reserva(uuid4()),
    )

    assert respuesta.status_code == 404


def test_reserva_rechaza_huesped_de_otro_tenant(client):
    tenant_huesped = uuid4()
    tenant_reserva = uuid4()
    huesped = crear_huesped(client, tenant_huesped)

    respuesta = client.post(
        "/api/v1/reservas/",
        headers={"X-Tenant-ID": str(tenant_reserva)},
        json=payload_reserva(huesped.json()["id"]),
    )

    assert huesped.status_code == 201
    assert respuesta.status_code == 404
