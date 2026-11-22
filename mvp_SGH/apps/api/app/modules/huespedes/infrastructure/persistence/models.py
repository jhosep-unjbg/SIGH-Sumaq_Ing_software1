from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Index, String, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class HuespedModel(Base):
    __tablename__ = "huespedes"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_huespedes_tenant_id_id"),
        Index("ix_huespedes_tenant_id", "tenant_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
    )
