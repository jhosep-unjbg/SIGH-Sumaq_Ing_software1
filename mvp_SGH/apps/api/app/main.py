"""
SUMAQ Hotel - API REST Centralizada
Punto de entrada de la aplicación FastAPI
"""

import time
import traceback
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Awaitable, Callable, Dict, List, Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import api_router
from app.common.observability import (
    REQUEST_ID_HEADER,
    configure_operational_logging,
)
from app.config.settings import settings
from app.infrastructure.database import engine

logger = configure_operational_logging()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    try:
        yield
    finally:
        await engine.dispose()

app = FastAPI(
    title="SUMAQ Hotel API",
    description="API REST Centralizada del Sistema de Gestión Hotelera SUMAQ",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[REQUEST_ID_HEADER],
)


def _request_id(request: Request) -> str:
    supplied_id = request.headers.get(REQUEST_ID_HEADER)
    if supplied_id and len(supplied_id) <= 36:
        try:
            return str(UUID(supplied_id))
        except ValueError:
            pass
    return str(uuid4())


def _error_code(status_code: int) -> str:
    if status_code >= 500:
        return "internal_error"
    return {
        400: "bad_request",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
        422: "validation_error",
    }.get(status_code, "http_error")


def _error_message(status_code: int) -> str:
    if status_code >= 500:
        return "Internal server error"
    return {
        400: "Invalid request",
        401: "Authentication failed",
        403: "Access denied",
        404: "Resource not found",
        409: "Request conflicts with current state",
        422: "Request validation failed",
    }.get(status_code, "Request failed")


def _error_payload(
    status_code: int,
    request_id: str,
    details: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, object]:
    error_payload: Dict[str, object] = {
        "code": _error_code(status_code),
        "message": _error_message(status_code),
    }
    payload: Dict[str, object] = {
        "error": error_payload,
        "request_id": request_id,
    }
    if details:
        error_payload["details"] = details
    return payload


def _route_group(request: Request) -> str:
    if request.url.path.startswith("/api/v1/"):
        return "api_v1"
    if request.url.path == "/health":
        return "health"
    return "other"


@app.exception_handler(StarletteHTTPException)
async def handle_http_exception(
    request: Request,
    error: StarletteHTTPException,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None) or str(uuid4())
    return JSONResponse(
        status_code=error.status_code,
        content=_error_payload(error.status_code, request_id),
        headers={**(error.headers or {}), REQUEST_ID_HEADER: request_id},
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_exception(
    request: Request,
    error: RequestValidationError,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None) or str(uuid4())
    details = [
        {
            "field": ".".join(str(part) for part in item.get("loc", ())),
            "code": str(item.get("type", "invalid")),
        }
        for item in error.errors()
    ]
    return JSONResponse(
        status_code=422,
        content=_error_payload(
            422,
            request_id,
            details,
        ),
        headers={REQUEST_ID_HEADER: request_id},
    )


@app.middleware("http")
async def request_logging_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = _request_id(request)
    request.state.request_id = request_id
    started_at = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as error:
        frames = traceback.extract_tb(error.__traceback__)
        origin = (
            f"{frames[-1].name}:{frames[-1].lineno}"
            if frames
            else "unknown"
        )
        duration_ms = (time.perf_counter() - started_at) * 1000
        route = _route_group(request)
        logger.error(
            "request_id=%s request.failed method=%s route_group=%s "
            "status_code=500 error_code=internal_error duration_ms=%.2f "
            "exception_type=%s origin=%s",
            request_id,
            request.method,
            route,
            duration_ms,
            type(error).__name__,
            origin,
        )
        response = JSONResponse(
            status_code=500,
            content=_error_payload(
                500,
                request_id,
            ),
        )
    else:
        duration_ms = (time.perf_counter() - started_at) * 1000
        route = _route_group(request)
        log_method = (
            logger.error
            if response.status_code >= 500
            else logger.warning
            if response.status_code >= 400
            else logger.info
        )
        log_method(
            "request_id=%s request.completed method=%s route_group=%s "
            "status_code=%d error_code=%s duration_ms=%.2f",
            request_id,
            request.method,
            route,
            response.status_code,
            _error_code(response.status_code)
            if response.status_code >= 400
            else "-",
            duration_ms,
        )

    response.headers[REQUEST_ID_HEADER] = request_id
    return response


# Incluir todos los routers de módulos
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "sumaq-api", "version": "1.0.0"}
