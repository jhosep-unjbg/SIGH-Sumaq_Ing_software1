from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Header, status
from app.common.exceptions import DomainError, domain_error_to_http
from app.modules.operacion_habitaciones.application.dto.tarea_dto import CrearTareaDTO
from app.modules.operacion_habitaciones.application.use_cases.crear_tarea import CrearTareaUseCase
from app.modules.operacion_habitaciones.application.use_cases.completar_tarea import CompletarTareaUseCase
from app.modules.operacion_habitaciones.presentation.schemas import CrearTareaRequest, TareaResponse
from app.modules.operacion_habitaciones.presentation.dependencies import (
    get_crear_tarea_uc, get_completar_tarea_uc, get_tarea_repo,
)
from app.modules.operacion_habitaciones.domain.repositories.tarea_repository import ITareaRepository

router = APIRouter()

@router.post("/", response_model=TareaResponse, status_code=status.HTTP_201_CREATED)
async def crear_tarea(payload: CrearTareaRequest, x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                      uc: CrearTareaUseCase = Depends(get_crear_tarea_uc)):
    try:
        return await uc.execute(CrearTareaDTO(**payload.model_dump()), x_tenant_id)
    except DomainError as e:
        raise domain_error_to_http(e)

@router.post("/{tarea_id}/completar", response_model=TareaResponse)
async def completar_tarea(tarea_id: UUID, x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                          uc: CompletarTareaUseCase = Depends(get_completar_tarea_uc)):
    try:
        return await uc.execute(tarea_id, x_tenant_id)
    except DomainError as e:
        raise domain_error_to_http(e)

@router.get("/", response_model=List[TareaResponse])
async def listar_tareas(x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                        repo: ITareaRepository = Depends(get_tarea_repo)):
    items = await repo.list_by_tenant(x_tenant_id)
    return [TareaResponse(id=t.id, tenant_id=t.tenant_id, habitacion_id=t.habitacion_id,
                          asignado_a=t.asignado_a, estado=t.estado.value, notas=t.notas,
                          created_at=t.created_at, updated_at=t.updated_at, completada_at=t.completada_at)
            for t in items]
