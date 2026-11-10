from fastapi import Depends
from app.modules.identidad_acceso.domain.repositories.usuario_repository import IUsuarioRepository
from app.modules.identidad_acceso.infrastructure.repositories.usuario_repository_impl import UsuarioRepositoryImpl
from app.modules.identidad_acceso.application.use_cases.crear_usuario import CrearUsuarioUseCase
from app.modules.identidad_acceso.application.use_cases.login import LoginUseCase

def get_usuario_repo() -> IUsuarioRepository:
    return UsuarioRepositoryImpl()
def get_crear_usuario_uc(repo=Depends(get_usuario_repo)):
    return CrearUsuarioUseCase(repo)
def get_login_uc(repo=Depends(get_usuario_repo)):
    return LoginUseCase(repo)
