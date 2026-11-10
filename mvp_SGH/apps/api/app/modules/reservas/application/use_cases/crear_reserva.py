"""
Caso de uso: Crear Reserva
"""

from datetime import date
from uuid import UUID

from app.common.exceptions import ConflictError, DomainError
from app.modules.reservas.domain.entities.reserva import Reserva
from app.modules.reservas.domain.repositories.reserva_repository import IReservaRepository
from app.modules.reservas.application.dto.reserva_dto import CrearReservaDTO, ReservaResponseDTO


class CrearReservaUseCase:
    def __init__(self, reserva_repo: IReservaRepository):
        self._reserva_repo = reserva_repo

    async def execute(self, dto: CrearReservaDTO, tenant_id: UUID) -> ReservaResponseDTO:
        # 1. Verificar disponibilidad (evitar dobles reservas)
        hay_conflicto = await self._reserva_repo.existe_conflicto(
            tenant_id=tenant_id,
            habitacion_id=dto.habitacion_id,
            fecha_entrada=dto.fecha_entrada,
            fecha_salida=dto.fecha_salida,
        )
        if hay_conflicto:
            raise ConflictError(
                "La habitación no está disponible en el rango de fechas solicitado"
            )

        # 2. Crear entidad de dominio
        try:
            reserva = Reserva.crear(
                tenant_id=tenant_id,
                habitacion_id=dto.habitacion_id,
                huesped_id=dto.huesped_id,
                fecha_entrada=dto.fecha_entrada,
                fecha_salida=dto.fecha_salida,
                precio_total=dto.precio_total,
                moneda=dto.moneda,
                notas=dto.notas,
            )
        except ValueError as e:
            raise DomainError(str(e))

        # 3. Persistir
        reserva_guardada = await self._reserva_repo.save(reserva)

        # 4. Mapear a DTO de respuesta
        return ReservaResponseDTO.from_entity(reserva_guardada)
