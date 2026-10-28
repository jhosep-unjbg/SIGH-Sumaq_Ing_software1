from fastapi import Depends
from app.modules.cuentas_pagos.domain.repositories.cuenta_repository import ICuentaRepository
from app.modules.cuentas_pagos.infrastructure.repositories.cuenta_repository_impl import CuentaRepositoryImpl
from app.modules.cuentas_pagos.application.use_cases.crear_cargo import CrearCargoUseCase
from app.modules.cuentas_pagos.application.use_cases.registrar_pago import RegistrarPagoUseCase
from app.modules.cuentas_pagos.application.use_cases.consultar_saldo import ConsultarSaldoUseCase

def get_cuenta_repo() -> ICuentaRepository:
    return CuentaRepositoryImpl()
def get_crear_cargo_uc(repo=Depends(get_cuenta_repo)):
    return CrearCargoUseCase(repo)
def get_registrar_pago_uc(repo=Depends(get_cuenta_repo)):
    return RegistrarPagoUseCase(repo)
def get_consultar_saldo_uc(repo=Depends(get_cuenta_repo)):
    return ConsultarSaldoUseCase(repo)
