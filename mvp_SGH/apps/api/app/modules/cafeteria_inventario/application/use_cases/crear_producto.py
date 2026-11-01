"""Caso de uso para crear un producto de inventario."""

from uuid import UUID

from app.common.exceptions import DomainError
from app.modules.cafeteria_inventario.application.dto.producto_dto import (
    CrearProductoDTO,
    ProductoResponseDTO,
)
from app.modules.cafeteria_inventario.domain.entities.producto import Producto
from app.modules.cafeteria_inventario.domain.repositories.producto_repository import (
    IProductoRepository,
)


class CrearProductoUseCase:
    """Crea y guarda un producto."""

    def __init__(self, repo: IProductoRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        dto: CrearProductoDTO,
        tenant_id: UUID,
    ) -> ProductoResponseDTO:
        """Crea un producto con los datos recibidos."""
        try:
            producto = Producto.crear(
                tenant_id=tenant_id,
                nombre=dto.nombre,
                precio=dto.precio,
                stock=dto.stock,
                categoria=dto.categoria,
            )
        except ValueError as error:
            raise DomainError(str(error)) from error

        producto_guardado = await self._repo.save(producto)
        return ProductoResponseDTO.from_entity(producto_guardado)