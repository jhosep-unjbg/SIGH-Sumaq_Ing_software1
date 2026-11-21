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


def registrar_huesped(client, tenant_id):
    respuesta = client.post(
        "/api/v1/huespedes/",
        headers={"X-Tenant-ID": tenant_id},
        json={"nombre": "Huésped de prueba"},
    )
    assert respuesta.status_code == 201
    return respuesta.json()["id"]


def payload():
    return {
        "habitacion_id": str(uuid4()),
        "huesped_id": str(uuid4()),
        "fecha_entrada": "2030-12-01",
        "fecha_salida": "2030-12-05",
        "precio_total": 800,
        "moneda": "PEN",
        "notas": "Prueba automatizada",
    }


def test_crear_y_consultar_reserva(client):
    tenant = str(uuid4())
    headers = {"X-Tenant-ID": tenant}
    datos = payload()
    datos["huesped_id"] = registrar_huesped(client, tenant)

    creada = client.post("/api/v1/reservas/", headers=headers, json=datos)

    assert creada.status_code == 201
    reserva_id = creada.json()["id"]

    consulta = client.get(f"/api/v1/reservas/{reserva_id}", headers=headers)
    assert consulta.status_code == 200
    assert consulta.json()["id"] == reserva_id


def test_rechazar_reserva_con_fechas_que_se_solapan(client):
    tenant = str(uuid4())
    headers = {"X-Tenant-ID": tenant}
    datos = payload()
    datos["huesped_id"] = registrar_huesped(client, tenant)

    primera = client.post("/api/v1/reservas/", headers=headers, json=datos)
    duplicada = client.post("/api/v1/reservas/", headers=headers, json=datos)

    assert primera.status_code == 201
    assert duplicada.status_code == 409


def test_reservas_aisladas_por_tenant(client):
    tenant = str(uuid4())
    otro_tenant = str(uuid4())
    datos = payload()
    datos["huesped_id"] = registrar_huesped(client, tenant)

    creada = client.post(
        "/api/v1/reservas/",
        headers={"X-Tenant-ID": tenant},
        json=datos,
    )
    reserva_id = creada.json()["id"]

    listado_otro_tenant = client.get(
        "/api/v1/reservas/",
        headers={"X-Tenant-ID": otro_tenant},
    )
    consulta_otro_tenant = client.get(
        f"/api/v1/reservas/{reserva_id}",
        headers={"X-Tenant-ID": otro_tenant},
    )

    assert listado_otro_tenant.status_code == 200
    assert listado_otro_tenant.json() == []
    assert consulta_otro_tenant.status_code == 404


def test_rechazar_salida_anterior_a_entrada(client):
    datos = payload()
    datos["fecha_salida"] = datos["fecha_entrada"]

    respuesta = client.post(
        "/api/v1/reservas/",
        headers={"X-Tenant-ID": str(uuid4())},
        json=datos,
    )

    assert respuesta.status_code == 400


def test_rechazar_reserva_con_solapamiento_parcial(client):
    tenant = str(uuid4())
    headers = {"X-Tenant-ID": tenant}
    primera_payload = payload()
    primera_payload["huesped_id"] = registrar_huesped(client, tenant)
    segunda_payload = payload()

    segunda_payload["habitacion_id"] = primera_payload["habitacion_id"]
    segunda_payload["huesped_id"] = primera_payload["huesped_id"]
    segunda_payload["fecha_entrada"] = "2030-12-04"
    segunda_payload["fecha_salida"] = "2030-12-08"

    primera = client.post(
        "/api/v1/reservas/",
        headers=headers,
        json=primera_payload,
    )
    segunda = client.post(
        "/api/v1/reservas/",
        headers=headers,
        json=segunda_payload,
    )

    assert primera.status_code == 201
    assert segunda.status_code == 409

def test_rechazar_reserva_con_huesped_inexistente(client):
    respuesta = client.post(
        "/api/v1/reservas/",
        headers={"X-Tenant-ID": str(uuid4())},
        json=payload(),
    )

    assert respuesta.status_code == 404