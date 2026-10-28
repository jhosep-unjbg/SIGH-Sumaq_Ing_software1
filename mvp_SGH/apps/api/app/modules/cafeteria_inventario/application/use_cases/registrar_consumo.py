from uuid import UUID
from app.common.exceptions import DomainError, NotFoundError
from app.modules.cafeteria_inventario.domain.entities.consumo import Consumo
from app.modules.cafeteria_inventario.domain.repositories.producto_repository import IProductoRepository
from app.modules.cafeteria_inventario.application.dto.producto_dto import RegistrarConsumoDTO, ConsumoResponseDTO

class RegistrarConsumoUseCase:
    def __init__(self, repo: IProductoRepository):
        self._repo = repo
    async def execute(self, dto: RegistrarConsumoDTO, tenant_id: UUID) -> ConsumoResponseDTO:
        producto = await self._repo.get_by_id(dto.producto_id, tenant_id)
        if not producto:
            raise NotFoundError("Producto no encontrado")
        try:
            producto.descontar_stock(dto.cantidad)
            consumo = Consumo.crear(tenant_id, dto.estadia_id, dto.producto_id,
                                    dto.cantidad, producto.precio)
        except ValueError as e:
            raise DomainError(str(e))
        await self._repo.save(producto)
        saved = await self._repo.save_consumo(consumo)
        return ConsumoResponseDTO.from_entity(saved)
