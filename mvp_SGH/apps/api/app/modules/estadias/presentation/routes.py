from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Header, status
from app.common.exceptions import DomainError, domain_error_to_http
from app.modules.estadias.application.dto.estadia_dto import CrearEstadiaDTO
from app.modules.estadias.application.use_cases.crear_estadia import CrearEstadiaUseCase
from app.modules.estadias.application.use_cases.check_in import CheckInUseCase
from app.modules.estadias.application.use_cases.check_out import CheckOutUseCase
from app.modules.estadias.presentation.schemas import CrearEstadiaRequest, EstadiaResponse
from app.modules.estadias.presentation.dependencies import (
    get_crear_estadia_uc, get_check_in_uc, get_check_out_uc, get_estadia_repo,
)
from app.modules.estadias.domain.repositories.estadia_repository import IEstadiaRepository

router = APIRouter()

@router.post("/", response_model=EstadiaResponse, status_code=status.HTTP_201_CREATED)
async def crear_estadia(
    payload: CrearEstadiaRequest,
    x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
    uc: CrearEstadiaUseCase = Depends(get_crear_estadia_uc),
):
    try:
        dto = CrearEstadiaDTO(**payload.model_dump())
        return await uc.execute(dto, x_tenant_id)
    except DomainError as e:
        raise domain_error_to_http(e)

@router.post("/{estadia_id}/check-in", response_model=EstadiaResponse)
async def check_in(
    estadia_id: UUID,
    x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
    uc: CheckInUseCase = Depends(get_check_in_uc),
):
    try:
        return await uc.execute(estadia_id, x_tenant_id)
    except DomainError as e:
        raise domain_error_to_http(e)

@router.post("/{estadia_id}/check-out", response_model=EstadiaResponse)
async def check_out(
    estadia_id: UUID,
    x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
    uc: CheckOutUseCase = Depends(get_check_out_uc),
):
    try:
        return await uc.execute(estadia_id, x_tenant_id)
    except DomainError as e:
        raise domain_error_to_http(e)

@router.get("/", response_model=List[EstadiaResponse])
async def listar_estadias(
    x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
    repo: IEstadiaRepository = Depends(get_estadia_repo),
):
    items = await repo.list_by_tenant(x_tenant_id)
    return [
        EstadiaResponse(
            id=e.id, tenant_id=e.tenant_id, reserva_id=e.reserva_id,
            habitacion_id=e.habitacion_id, huesped_id=e.huesped_id,
            fecha_entrada=e.fecha_entrada, fecha_salida=e.fecha_salida,
            estado=e.estado.value, checked_in_at=e.checked_in_at,
            checked_out_at=e.checked_out_at, created_at=e.created_at,
            updated_at=e.updated_at,
        ) for e in items
    ]
