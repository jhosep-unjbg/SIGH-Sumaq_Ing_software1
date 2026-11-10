"""
SUMAQ Hotel - API REST Centralizada
Punto de entrada de la aplicación FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.config.settings import settings

app = FastAPI(
    title="SUMAQ Hotel API",
    description="API REST Centralizada del Sistema de Gestión Hotelera SUMAQ",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos los routers de módulos
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "sumaq-api", "version": "1.0.0"}
