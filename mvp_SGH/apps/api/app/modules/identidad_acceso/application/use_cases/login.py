"""Caso de uso para autenticar un usuario."""

from uuid import UUID

from app.common.exceptions import UnauthorizedError
from app.modules.identidad_acceso.application.dto.usuario_dto import (
    LoginDTO,
    TokenResponseDTO,
    UsuarioResponseDTO,
)
from app.modules.identidad_acceso.domain.repositories.usuario_repository import (
    IUsuarioRepository,
)


class LoginUseCase:
    """Valida credenciales y genera el token simulado del MVP."""

    _MENSAJE_CREDENCIALES_INVALIDAS = "Credenciales inválidas"

    def __init__(self, repo: IUsuarioRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        dto: LoginDTO,
        tenant_id: UUID,
    ) -> TokenResponseDTO:
        """Autentica al usuario dentro del hotel indicado."""
        usuario = await self._repo.get_by_email(dto.email, tenant_id)
        if usuario is None or not usuario.activo:
            raise UnauthorizedError(self._MENSAJE_CREDENCIALES_INVALIDAS)

        password_hash_esperado = f"hashed:{dto.password}"
        if usuario.password_hash != password_hash_esperado:
            raise UnauthorizedError(self._MENSAJE_CREDENCIALES_INVALIDAS)

        # El token es simulado y solo corresponde al MVP.
        token = f"mvp-token-{usuario.id}-{tenant_id}"

        return TokenResponseDTO(
            access_token=token,
            usuario=UsuarioResponseDTO.from_entity(usuario),
        )