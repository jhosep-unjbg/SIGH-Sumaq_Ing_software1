from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Numeric,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class ReservaModel(Base):
    __tablename__ = "reservas"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "huesped_id"],
            ["huespedes.tenant_id", "huespedes.id"],
            name="fk_reservas_huesped_tenant",
        ),
        CheckConstraint(
            "fecha_salida > fecha_entrada",
            name="ck_reservas_fecha_salida_posterior",
        ),
        CheckConstraint("precio_total >= 0", name="ck_reservas_precio_no_negativo"),
        CheckConstraint(
            "estado IN ('pendiente', 'confirmada', 'cancelada', "
            "'checked_in', 'checked_out', 'no_show')",
            name="ck_reservas_estado_valido",
        ),
        Index(
            "ix_reservas_tenant_habitacion_fechas",
            "tenant_id",
            "habitacion_id",
            "fecha_entrada",
            "fecha_salida",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    habitacion_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    huesped_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    fecha_entrada: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_salida: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    precio_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    moneda: Mapped[str] = mapped_column(String(10), nullable=False)
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
