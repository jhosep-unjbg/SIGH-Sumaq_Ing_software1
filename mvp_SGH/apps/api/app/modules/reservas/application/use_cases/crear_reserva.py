"""Caso de uso para crear una reserva."""

from uuid import UUID

from app.common.exceptions import ConflictError, DomainError
from app.modules.reservas.application.dto.reserva_dto import (
    CrearReservaDTO,
    ReservaResponseDTO,
)
from app.modules.reservas.domain.entities.reserva import Reserva
from app.modules.reservas.domain.repositories.reserva_repository import (
    IReservaRepository,
)


class CrearReservaUseCase:
    """Coordina las validaciones y el registro de una reserva."""

    _MENSAJE_HABITACION_NO_DISPONIBLE = (
        "La habitación no está disponible en el rango de fechas solicitado"
    )

    def __init__(self, reserva_repo: IReservaRepository) -> None:
        self._reserva_repo = reserva_repo

    async def execute(
        self,
        dto: CrearReservaDTO,
        tenant_id: UUID,
    ) -> ReservaResponseDTO:
        """Crea una reserva si la habitación está disponible."""
        await self._validar_disponibilidad(dto, tenant_id)

        reserva = self._crear_entidad(dto, tenant_id)
        reserva_guardada = await self._reserva_repo.save(reserva)

        return ReservaResponseDTO.from_entity(reserva_guardada)

    async def _validar_disponibilidad(
        self,
        dto: CrearReservaDTO,
        tenant_id: UUID,
    ) -> None:
        hay_conflicto = await self._reserva_repo.existe_conflicto(
            tenant_id=tenant_id,
            habitacion_id=dto.habitacion_id,
            fecha_entrada=dto.fecha_entrada,
            fecha_salida=dto.fecha_salida,
        )
        if hay_conflicto:
            raise ConflictError(self._MENSAJE_HABITACION_NO_DISPONIBLE)

    @staticmethod
    def _crear_entidad(
        dto: CrearReservaDTO,
        tenant_id: UUID,
    ) -> Reserva:
        try:
            return Reserva.crear(
                tenant_id=tenant_id,
                habitacion_id=dto.habitacion_id,
                huesped_id=dto.huesped_id,
                fecha_entrada=dto.fecha_entrada,
                fecha_salida=dto.fecha_salida,
                precio_total=dto.precio_total,
                moneda=dto.moneda,
                notas=dto.notas,
            )
        except ValueError as error:
            raise DomainError(str(error)) from error