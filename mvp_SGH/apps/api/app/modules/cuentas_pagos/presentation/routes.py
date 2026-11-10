from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Header, Query, status
from app.common.exceptions import DomainError, domain_error_to_http
from app.modules.cuentas_pagos.application.dto.cuenta_dto import CrearCargoDTO, RegistrarPagoDTO
from app.modules.cuentas_pagos.domain.entities.cargo import TipoCargo
from app.modules.cuentas_pagos.application.use_cases.crear_cargo import CrearCargoUseCase
from app.modules.cuentas_pagos.application.use_cases.registrar_pago import RegistrarPagoUseCase
from app.modules.cuentas_pagos.application.use_cases.consultar_saldo import ConsultarSaldoUseCase
from app.modules.cuentas_pagos.presentation.schemas import (
    CrearCargoRequest, RegistrarPagoRequest, CargoResponse, PagoResponse, SaldoResponse,
)
from app.modules.cuentas_pagos.presentation.dependencies import (
    get_crear_cargo_uc, get_registrar_pago_uc, get_consultar_saldo_uc, get_cuenta_repo,
)
from app.modules.cuentas_pagos.domain.repositories.cuenta_repository import ICuentaRepository

router = APIRouter()

@router.post("/cargos", response_model=CargoResponse, status_code=status.HTTP_201_CREATED)
async def crear_cargo(payload: CrearCargoRequest, x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                      uc: CrearCargoUseCase = Depends(get_crear_cargo_uc)):
    try:
        tipo = TipoCargo(payload.tipo) if payload.tipo in TipoCargo._value2member_map_ else TipoCargo.OTRO
        dto = CrearCargoDTO(estadia_id=payload.estadia_id, descripcion=payload.descripcion,
                            monto=payload.monto, tipo=tipo)
        return await uc.execute(dto, x_tenant_id)
    except DomainError as e:
        raise domain_error_to_http(e)

@router.post("/pagos", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_pago(payload: RegistrarPagoRequest, x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                         uc: RegistrarPagoUseCase = Depends(get_registrar_pago_uc)):
    try:
        return await uc.execute(RegistrarPagoDTO(**payload.model_dump()), x_tenant_id)
    except DomainError as e:
        raise domain_error_to_http(e)

@router.get("/saldo/{estadia_id}", response_model=SaldoResponse)
async def consultar_saldo(estadia_id: UUID, x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                          uc: ConsultarSaldoUseCase = Depends(get_consultar_saldo_uc)):
    return await uc.execute(estadia_id, x_tenant_id)

@router.get("/cargos", response_model=List[CargoResponse])
async def listar_cargos(x_tenant_id: UUID = Header(..., alias="X-Tenant-ID"),
                        estadia_id: Optional[UUID] = Query(None),
                        repo: ICuentaRepository = Depends(get_cuenta_repo)):
    items = await repo.list_cargos(x_tenant_id, estadia_id)
    return [CargoResponse(id=c.id, tenant_id=c.tenant_id, estadia_id=c.estadia_id,
                          descripcion=c.descripcion, monto=c.monto, tipo=c.tipo.value,
                          estado=c.estado.value, created_at=c.created_at) for c in items]
