"""
Configuración central de la aplicación.
Carga variables de entorno.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "SUMAQ Hotel API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database (PostgreSQL Primary)
    DATABASE_URL: str = "postgresql+asyncpg://sumaq:sumaq@localhost:5432/sumaq_hotel"
    DATABASE_READ_URL: str = "postgresql+asyncpg://sumaq:sumaq@localhost:5433/sumaq_hotel"  # Réplica

    # JWT / Auth (consumido desde Auth Server segregado)
    JWT_PUBLIC_KEY_PATH: str = "keys/public.pem"
    JWT_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Multi-tenant
    TENANT_HEADER: str = "X-Tenant-ID"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
