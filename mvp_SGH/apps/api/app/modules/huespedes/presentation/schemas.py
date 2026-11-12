from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CrearHuespedRequest(BaseModel):
    nombre: str = Field(min_length=1)


class HuespedResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    nombre: str
    activo: bool
    created_at: datetime
