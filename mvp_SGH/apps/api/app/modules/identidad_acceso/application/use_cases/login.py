from uuid import UUID
from app.common.exceptions import UnauthorizedError
from app.modules.identidad_acceso.domain.repositories.usuario_repository import IUsuarioRepository
from app.modules.identidad_acceso.application.dto.usuario_dto import LoginDTO, TokenResponseDTO, UsuarioResponseDTO

class LoginUseCase:
    def __init__(self, repo: IUsuarioRepository):
        self._repo = repo
    async def execute(self, dto: LoginDTO, tenant_id: UUID) -> TokenResponseDTO:
        usuario = await self._repo.get_by_email(dto.email, tenant_id)
        if not usuario or not usuario.activo:
            raise UnauthorizedError("Credenciales inválidas")
        expected = f"hashed:{dto.password}"
        if usuario.password_hash != expected:
            raise UnauthorizedError("Credenciales inválidas")
        # MVP: token mock (en producción JWT RS256 desde Auth Server)
        token = f"mvp-token-{usuario.id}-{tenant_id}"
        return TokenResponseDTO(
            access_token=token,
            usuario=UsuarioResponseDTO.from_entity(usuario),
        )
