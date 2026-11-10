"""
Esquemas Pydantic para la capa de presentación (OpenAPI).
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CrearReservaRequest(BaseModel):
    habitacion_id: UUID
    huesped_id: UUID
    fecha_entrada: date
    fecha_salida: date
    precio_total: float = Field(ge=0, description="Precio total en la moneda indicada")
    moneda: str = Field(default="PEN", max_length=3)
    notas: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "habitacion_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "huesped_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
                "fecha_entrada": "2026-11-15",
                "fecha_salida": "2026-11-18",
                "precio_total": 450.00,
                "moneda": "PEN",
                "notas": "Llegada tarde"
            }
        }
    }


class ReservaResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    habitacion_id: UUID
    huesped_id: UUID
    fecha_entrada: date
    fecha_salida: date
    estado: str
    precio_total: float
    moneda: str
    notas: Optional[str]
    created_at: datetime
    updated_at: datetime
