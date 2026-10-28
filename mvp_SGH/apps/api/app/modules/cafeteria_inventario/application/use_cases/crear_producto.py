from uuid import UUID
from app.common.exceptions import DomainError
from app.modules.cafeteria_inventario.domain.entities.producto import Producto
from app.modules.cafeteria_inventario.domain.repositories.producto_repository import IProductoRepository
from app.modules.cafeteria_inventario.application.dto.producto_dto import CrearProductoDTO, ProductoResponseDTO

class CrearProductoUseCase:
    def __init__(self, repo: IProductoRepository):
        self._repo = repo
    async def execute(self, dto: CrearProductoDTO, tenant_id: UUID) -> ProductoResponseDTO:
        try:
            p = Producto.crear(tenant_id, dto.nombre, dto.precio, dto.stock, dto.categoria)
        except ValueError as e:
            raise DomainError(str(e))
        saved = await self._repo.save(p)
        return ProductoResponseDTO.from_entity(saved)
