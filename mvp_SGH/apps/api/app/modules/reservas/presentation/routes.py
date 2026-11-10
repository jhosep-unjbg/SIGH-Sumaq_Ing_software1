"""
Rutas HTTP del módulo de Reservas - MVP
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Header, status

from app.common.exceptions import DomainError, domain_error_to_http
from app.modules.reservas.application.dto.reserva_dto import CrearReservaDTO
from app.modules.reservas.application.use_cases.crear_reserva import CrearReservaUseCase
from app.modules.reservas.presentation.schemas import CrearReservaRequest, ReservaResponse
from app.modules.reservas.presentation.dependencies import (
    get_crear_reserva_use_case,
    get_reserva_repository,
)
from app.modules.reservas.domain.repositories.reserva_repository import IReservaRepository

router = APIRouter()


@router.post(
    "/",
    response_model=ReservaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva reserva",
)
async def crear_reserva(
    payload: CrearReservaRequest,
    x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
    use_case: CrearReservaUseCase = Depends(get_crear_reserva_use_case),
):
    """Crea una reserva atómica verificando disponibilidad de la habitación."""
    try:
        dto = CrearReservaDTO(
            habitacion_id=payload.habitacion_id,
            huesped_id=payload.huesped_id,
            fecha_entrada=payload.fecha_entrada,
            fecha_salida=payload.fecha_salida,
            precio_total=payload.precio_total,
            moneda=payload.moneda,
            notas=payload.notas,
        )
        result = await use_case.execute(dto, tenant_id=x_tenant_id)
        return result
    except DomainError as e:
        raise domain_error_to_http(e)


@router.get(
    "/",
    response_model=List[ReservaResponse],
    summary="Listar reservas del tenant",
)
async def listar_reservas(
    x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
    skip: int = 0,
    limit: int = 50,
    repo: IReservaRepository = Depends(get_reserva_repository),
):
    """Lista las reservas del hotel (tenant) actual."""
    reservas = await repo.list_by_tenant(tenant_id=x_tenant_id, skip=skip, limit=limit)
    return [
        ReservaResponse(
            id=r.id,
            tenant_id=r.tenant_id,
            habitacion_id=r.habitacion_id,
            huesped_id=r.huesped_id,
            fecha_entrada=r.fecha_entrada,
            fecha_salida=r.fecha_salida,
            estado=r.estado.value,
            precio_total=r.precio_total,
            moneda=r.moneda,
            notas=r.notas,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in reservas
    ]


@router.get(
    "/{reserva_id}",
    response_model=ReservaResponse,
    summary="Obtener una reserva por ID",
)
async def obtener_reserva(
    reserva_id: UUID,
    x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
    repo: IReservaRepository = Depends(get_reserva_repository),
):
    """Obtiene una reserva específica del tenant."""
    reserva = await repo.get_by_id(reserva_id, x_tenant_id)
    if not reserva:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return ReservaResponse(
        id=reserva.id,
        tenant_id=reserva.tenant_id,
        habitacion_id=reserva.habitacion_id,
        huesped_id=reserva.huesped_id,
        fecha_entrada=reserva.fecha_entrada,
        fecha_salida=reserva.fecha_salida,
        estado=reserva.estado.value,
        precio_total=reserva.precio_total,
        moneda=reserva.moneda,
        notas=reserva.notas,
        created_at=reserva.created_at,
        updated_at=reserva.updated_at,
    )
