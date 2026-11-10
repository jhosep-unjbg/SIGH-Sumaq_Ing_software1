"""
Enrutador principal de la API.
Agrega todos los routers de los Bounded Contexts.
"""

from fastapi import APIRouter

from app.modules.reservas.presentation.routes import router as reservas_router
from app.modules.estadias.presentation.routes import router as estadias_router
from app.modules.operacion_habitaciones.presentation.routes import router as operacion_router
from app.modules.cafeteria_inventario.presentation.routes import router as cafeteria_router
from app.modules.cuentas_pagos.presentation.routes import router as cuentas_router
from app.modules.identidad_acceso.presentation.routes import router as identidad_router

api_router = APIRouter()

api_router.include_router(reservas_router, prefix="/reservas", tags=["Reservas"])
api_router.include_router(estadias_router, prefix="/estadias", tags=["Estadías"])
api_router.include_router(operacion_router, prefix="/operacion-habitaciones", tags=["Operación Habitaciones"])
api_router.include_router(cafeteria_router, prefix="/cafeteria", tags=["Cafetería e Inventario"])
api_router.include_router(cuentas_router, prefix="/cuentas-pagos", tags=["Cuentas y Pagos"])
api_router.include_router(identidad_router, prefix="/identidad", tags=["Identidad y Acceso"])
