from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Header, status
from app.common.exceptions import DomainError, domain_error_to_http
from app.modules.identidad_acceso.application.dto.usuario_dto import CrearUsuarioDTO, LoginDTO
from app.modules.identidad_acceso.domain.entities.usuario import Rol
from app.modules.identidad_acceso.application.use_cases.crear_usuario import CrearUsuarioUseCase
from app.modules.identidad_acceso.application.use_cases.login import LoginUseCase
from app.modules.identidad_acceso.presentation.schemas import (
    CrearUsuarioRequest, LoginRequest, UsuarioResponse, TokenResponse,
)
from app.modules.identidad_acceso.presentation.dependencies import (
    get_crear_usuario_uc, get_login_uc, get_usuario_repo,
)
from app.modules.identidad_acceso.domain.repositories.usuario_repository import IUsuarioRepository

router = APIRouter()

@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(payload: CrearUsuarioRequest, x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                        uc: CrearUsuarioUseCase = Depends(get_crear_usuario_uc)):
    try:
        rol = Rol(payload.rol) if payload.rol in Rol._value2member_map_ else Rol.RECEPCION
        dto = CrearUsuarioDTO(email=payload.email, nombre=payload.nombre, rol=rol, password=payload.password)
        return await uc.execute(dto, x_tenant_id)
    except DomainError as e:
        raise domain_error_to_http(e)

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                uc: LoginUseCase = Depends(get_login_uc)):
    try:
        return await uc.execute(LoginDTO(email=payload.email, password=payload.password), x_tenant_id)
    except DomainError as e:
        raise domain_error_to_http(e)

@router.get("/usuarios", response_model=List[UsuarioResponse])
async def listar_usuarios(x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                          repo: IUsuarioRepository = Depends(get_usuario_repo)):
    items = await repo.list_by_tenant(x_tenant_id)
    return [UsuarioResponse(id=u.id, tenant_id=u.tenant_id, email=u.email, nombre=u.nombre,
                            rol=u.rol.value, activo=u.activo, created_at=u.created_at) for u in items]
