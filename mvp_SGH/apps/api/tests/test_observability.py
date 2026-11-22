from uuid import UUID, uuid4

from app.main import app
from app.modules.reservas.presentation.dependencies import get_reserva_repository


def test_domain_error_uses_normalized_response_and_request_id(client):
    request_id = str(uuid4())
    response = client.post(
        "/api/v1/reservas/",
        headers={
            "X-Tenant-ID": str(uuid4()),
            "X-Request-ID": request_id,
        },
        json={
            "habitacion_id": str(uuid4()),
            "huesped_id": str(uuid4()),
            "fecha_entrada": "2030-12-01",
            "fecha_salida": "2030-12-05",
            "precio_total": 800,
            "moneda": "PEN",
        },
    )

    assert response.status_code == 404
    assert response.headers["X-Request-ID"] == request_id
    assert response.json() == {
        "error": {
            "code": "not_found",
            "message": "Resource not found",
        },
        "request_id": request_id,
    }


def test_validation_error_does_not_echo_invalid_input(client):
    request_id = str(uuid4())
    sensitive_input = "customer-private-value"
    response = client.post(
        "/api/v1/reservas/",
        headers={
            "X-Tenant-ID": str(uuid4()),
            "X-Request-ID": request_id,
        },
        json={"habitacion_id": sensitive_input},
    )

    assert response.status_code == 422
    assert response.headers["X-Request-ID"] == request_id
    assert response.json()["error"]["code"] == "validation_error"
    assert sensitive_input not in response.text
    assert "input" not in response.text


def test_invalid_request_id_is_replaced_with_uuid(client):
    supplied_id = "not-a-uuid"
    response = client.get(
        "/health",
        headers={"X-Request-ID": supplied_id},
    )
    response_id = response.headers["X-Request-ID"]

    assert response.status_code == 200
    assert response_id != supplied_id
    assert str(UUID(response_id)) == response_id


def test_unhandled_error_is_sanitized_and_logged_without_exception_text(
    client,
    caplog,
    monkeypatch,
):
    request_id = str(uuid4())
    sensitive_error = "database-password-must-not-be-logged"

    class FailingRepository:
        async def list_by_tenant(self, **kwargs):
            del kwargs
            raise RuntimeError(sensitive_error)

    monkeypatch.setitem(
        app.dependency_overrides,
        get_reserva_repository,
        lambda: FailingRepository(),
    )
    response = client.get(
        "/api/v1/reservas/",
        headers={
            "X-Tenant-ID": str(uuid4()),
            "X-Request-ID": request_id,
            "Authorization": f"Bearer {sensitive_error}",
        },
    )
    logs = "\n".join(
        record.getMessage()
        for record in caplog.records
        if record.name == "sumaq.api"
    )

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "internal_error",
            "message": "Internal server error",
        },
        "request_id": request_id,
    }
    assert sensitive_error not in response.text
    assert sensitive_error not in logs
    assert f"request_id={request_id}" in logs
    assert "request.failed" in logs
    assert "route_group=api_v1" in logs
