from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Header, status

from app.common.exceptions import DomainError, domain_error_to_http
from app.modules.huespedes.application.dto.huesped_dto import CrearHuespedDTO
from app.modules.huespedes.application.use_cases.crear_huesped import CrearHuespedUseCase
from app.modules.huespedes.domain.repositories.huesped_repository import IHuespedRepository
from app.modules.huespedes.presentation.dependencies import (
    get_crear_huesped_use_case,
    get_huesped_repository,
)
from app.modules.huespedes.presentation.schemas import CrearHuespedRequest, HuespedResponse

router = APIRouter()


@router.post(
    "/",
    response_model=HuespedResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un huésped",
)
async def crear_huesped(
    payload: CrearHuespedRequest,
    x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
    use_case: CrearHuespedUseCase = Depends(get_crear_huesped_use_case),
):
    try:
        return await use_case.execute(CrearHuespedDTO(nombre=payload.nombre), x_tenant_id)
    except DomainError as error:
        raise domain_error_to_http(error)


@router.get("/", response_model=List[HuespedResponse], summary="Listar huéspedes del tenant")
async def listar_huespedes(
    x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
    repo: IHuespedRepository = Depends(get_huesped_repository),
):
    huespedes = await repo.list_by_tenant(x_tenant_id)
    return [
        HuespedResponse(
            id=huesped.id,
            tenant_id=huesped.tenant_id,
            nombre=huesped.nombre,
            activo=huesped.activo,
            created_at=huesped.created_at,
        )
        for huesped in huespedes
    ]
