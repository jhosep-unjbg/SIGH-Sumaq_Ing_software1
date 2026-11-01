"""Caso de uso para crear un usuario del hotel."""

from uuid import UUID

from app.common.exceptions import ConflictError
from app.modules.identidad_acceso.application.dto.usuario_dto import (
    CrearUsuarioDTO,
    UsuarioResponseDTO,
)
from app.modules.identidad_acceso.domain.entities.usuario import Usuario
from app.modules.identidad_acceso.domain.repositories.usuario_repository import (
    IUsuarioRepository,
)


class CrearUsuarioUseCase:
    """Valida la unicidad del correo y registra un usuario."""

    _MENSAJE_EMAIL_DUPLICADO = "Ya existe un usuario con ese email"

    def __init__(self, repo: IUsuarioRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        dto: CrearUsuarioDTO,
        tenant_id: UUID,
    ) -> UsuarioResponseDTO:
        """Crea un usuario si el correo aún no está registrado."""
        usuario_existente = await self._repo.get_by_email(dto.email, tenant_id)
        if usuario_existente is not None:
            raise ConflictError(self._MENSAJE_EMAIL_DUPLICADO)

        # El MVP usa un hash simulado; debe sustituirse por un algoritmo seguro
        # antes de utilizar este flujo en un entorno real.
        password_hash = f"hashed:{dto.password}"
        usuario = Usuario.crear(
            tenant_id=tenant_id,
            email=dto.email,
            nombre=dto.nombre,
            rol=dto.rol,
            password_hash=password_hash,
        )

        usuario_guardado = await self._repo.save(usuario)
        return UsuarioResponseDTO.from_entity(usuario_guardado)