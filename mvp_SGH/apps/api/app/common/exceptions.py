"""
Excepciones de dominio y aplicación compartidas.
"""

from fastapi import HTTPException, status


class DomainError(Exception):
    """Error de reglas de negocio del dominio."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class UnauthorizedError(DomainError):
    pass


class ForbiddenError(DomainError):
    pass


def domain_error_to_http(exc: DomainError) -> HTTPException:
    """Mapea errores de dominio a respuestas HTTP."""
    if isinstance(exc, NotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    if isinstance(exc, ConflictError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)
    if isinstance(exc, UnauthorizedError):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.message)
    if isinstance(exc, ForbiddenError):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
