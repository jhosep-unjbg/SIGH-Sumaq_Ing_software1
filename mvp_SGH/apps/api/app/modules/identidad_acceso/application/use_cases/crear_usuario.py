from uuid import UUID
from app.common.exceptions import ConflictError
from app.modules.identidad_acceso.domain.entities.usuario import Usuario
from app.modules.identidad_acceso.domain.repositories.usuario_repository import IUsuarioRepository
from app.modules.identidad_acceso.application.dto.usuario_dto import CrearUsuarioDTO, UsuarioResponseDTO

class CrearUsuarioUseCase:
    def __init__(self, repo: IUsuarioRepository):
        self._repo = repo
    async def execute(self, dto: CrearUsuarioDTO, tenant_id: UUID) -> UsuarioResponseDTO:
        existing = await self._repo.get_by_email(dto.email, tenant_id)
        if existing:
            raise ConflictError("Ya existe un usuario con ese email")
        # MVP: hash simple (en producción usar bcrypt)
        password_hash = f"hashed:{dto.password}"
        usuario = Usuario.crear(tenant_id, dto.email, dto.nombre, dto.rol, password_hash)
        saved = await self._repo.save(usuario)
        return UsuarioResponseDTO.from_entity(saved)
