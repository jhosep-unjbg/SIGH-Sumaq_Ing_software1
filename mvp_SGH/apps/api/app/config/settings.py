"""
Configuración central de la aplicación.
Carga configuración desde variables de entorno.
"""

from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        str_strip_whitespace=True,
    )

    # App
    APP_NAME: str = "SUMAQ Hotel API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database (PostgreSQL Primary)
    DATABASE_URL: str = Field(min_length=1)
    DATABASE_READ_URL: Optional[str] = None  # Réplica opcional

    # JWT / Auth (consumido desde Auth Server segregado)
    JWT_PUBLIC_KEY_PATH: str = "keys/public.pem"
    JWT_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Multi-tenant
    TENANT_HEADER: str = "X-Tenant-ID"


settings = Settings()
