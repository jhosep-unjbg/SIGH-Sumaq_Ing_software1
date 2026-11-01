"""Caso de uso para registrar un consumo de inventario."""

from uuid import UUID

from app.common.exceptions import DomainError, NotFoundError
from app.modules.cafeteria_inventario.application.dto.producto_dto import (
    ConsumoResponseDTO,
    RegistrarConsumoDTO,
)
from app.modules.cafeteria_inventario.domain.entities.consumo import Consumo
from app.modules.cafeteria_inventario.domain.repositories.producto_repository import (
    IProductoRepository,
)


class RegistrarConsumoUseCase:
    """Registra el consumo y descuenta las unidades del producto."""

    def __init__(self, repo: IProductoRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        dto: RegistrarConsumoDTO,
        tenant_id: UUID,
    ) -> ConsumoResponseDTO:
        """Registra el consumo para la estadía indicada."""
        producto = await self._repo.get_by_id(dto.producto_id, tenant_id)
        if producto is None:
            raise NotFoundError("Producto no encontrado")

        try:
            producto.descontar_stock(dto.cantidad)
            consumo = Consumo.crear(
                tenant_id=tenant_id,
                estadia_id=dto.estadia_id,
                producto_id=dto.producto_id,
                cantidad=dto.cantidad,
                precio_unitario=producto.precio,
            )
        except ValueError as error:
            raise DomainError(str(error)) from error

        await self._repo.save(producto)
        consumo_guardado = await self._repo.save_consumo(consumo)

        return ConsumoResponseDTO.from_entity(consumo_guardado)