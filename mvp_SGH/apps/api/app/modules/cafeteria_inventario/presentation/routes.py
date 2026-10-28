from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Header, status
from app.common.exceptions import DomainError, domain_error_to_http
from app.modules.cafeteria_inventario.application.dto.producto_dto import CrearProductoDTO, RegistrarConsumoDTO
from app.modules.cafeteria_inventario.application.use_cases.crear_producto import CrearProductoUseCase
from app.modules.cafeteria_inventario.application.use_cases.registrar_consumo import RegistrarConsumoUseCase
from app.modules.cafeteria_inventario.presentation.schemas import (
    CrearProductoRequest, RegistrarConsumoRequest, ProductoResponse, ConsumoResponse,
)
from app.modules.cafeteria_inventario.presentation.dependencies import (
    get_crear_producto_uc, get_registrar_consumo_uc, get_producto_repo,
)
from app.modules.cafeteria_inventario.domain.repositories.producto_repository import IProductoRepository

router = APIRouter()

@router.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(payload: CrearProductoRequest, x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                         uc: CrearProductoUseCase = Depends(get_crear_producto_uc)):
    try:
        return await uc.execute(CrearProductoDTO(**payload.model_dump()), x_tenant_id)
    except DomainError as e:
        raise domain_error_to_http(e)

@router.get("/productos", response_model=List[ProductoResponse])
async def listar_productos(x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                           repo: IProductoRepository = Depends(get_producto_repo)):
    items = await repo.list_by_tenant(x_tenant_id)
    return [ProductoResponse(id=p.id, tenant_id=p.tenant_id, nombre=p.nombre, precio=p.precio,
                             stock=p.stock, categoria=p.categoria, activo=p.activo, created_at=p.created_at)
            for p in items]

@router.post("/consumos", response_model=ConsumoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_consumo(payload: RegistrarConsumoRequest, x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                            uc: RegistrarConsumoUseCase = Depends(get_registrar_consumo_uc)):
    try:
        return await uc.execute(RegistrarConsumoDTO(**payload.model_dump()), x_tenant_id)
    except DomainError as e:
        raise domain_error_to_http(e)

@router.get("/consumos", response_model=List[ConsumoResponse])
async def listar_consumos(x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                          repo: IProductoRepository = Depends(get_producto_repo)):
    items = await repo.list_consumos(x_tenant_id)
    return [ConsumoResponse(id=c.id, tenant_id=c.tenant_id, estadia_id=c.estadia_id,
                            producto_id=c.producto_id, cantidad=c.cantidad,
                            precio_unitario=c.precio_unitario, total=c.total, created_at=c.created_at)
            for c in items]
