"""Create guest and reservation tables.

Revision ID: 20261121_0001
Revises:
Create Date: 2026-11-21
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261121_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "huespedes",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("tenant_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("nombre", sa.String(length=200), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=False),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_huespedes_tenant_id_id"),
    )
    op.create_index("ix_huespedes_tenant_id", "huespedes", ["tenant_id"])

    op.create_table(
        "reservas",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("tenant_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("habitacion_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("huesped_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("fecha_entrada", sa.Date(), nullable=False),
        sa.Column("fecha_salida", sa.Date(), nullable=False),
        sa.Column("estado", sa.String(length=20), nullable=False),
        sa.Column("precio_total", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("moneda", sa.String(length=10), nullable=False),
        sa.Column("notas", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=False),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=False),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "fecha_salida > fecha_entrada",
            name="ck_reservas_fecha_salida_posterior",
        ),
        sa.CheckConstraint(
            "precio_total >= 0",
            name="ck_reservas_precio_no_negativo",
        ),
        sa.CheckConstraint(
            "estado IN ('pendiente', 'confirmada', 'cancelada', "
            "'checked_in', 'checked_out', 'no_show')",
            name="ck_reservas_estado_valido",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "huesped_id"],
            ["huespedes.tenant_id", "huespedes.id"],
            name="fk_reservas_huesped_tenant",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_reservas_tenant_habitacion_fechas",
        "reservas",
        ["tenant_id", "habitacion_id", "fecha_entrada", "fecha_salida"],
    )


def downgrade() -> None:
    op.drop_index("ix_reservas_tenant_habitacion_fechas", table_name="reservas")
    op.drop_table("reservas")
    op.drop_index("ix_huespedes_tenant_id", table_name="huespedes")
    op.drop_table("huespedes")
