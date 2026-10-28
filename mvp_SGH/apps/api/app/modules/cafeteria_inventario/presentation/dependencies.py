from fastapi import Depends
from app.modules.cafeteria_inventario.domain.repositories.producto_repository import IProductoRepository
from app.modules.cafeteria_inventario.infrastructure.repositories.producto_repository_impl import ProductoRepositoryImpl
from app.modules.cafeteria_inventario.application.use_cases.crear_producto import CrearProductoUseCase
from app.modules.cafeteria_inventario.application.use_cases.registrar_consumo import RegistrarConsumoUseCase

def get_producto_repo() -> IProductoRepository:
    return ProductoRepositoryImpl()
def get_crear_producto_uc(repo=Depends(get_producto_repo)):
    return CrearProductoUseCase(repo)
def get_registrar_consumo_uc(repo=Depends(get_producto_repo)):
    return RegistrarConsumoUseCase(repo)
