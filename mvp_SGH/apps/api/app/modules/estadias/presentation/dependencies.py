from fastapi import Depends
from app.modules.estadias.domain.repositories.estadia_repository import IEstadiaRepository
from app.modules.estadias.infrastructure.repositories.estadia_repository_impl import EstadiaRepositoryImpl
from app.modules.estadias.application.use_cases.crear_estadia import CrearEstadiaUseCase
from app.modules.estadias.application.use_cases.check_in import CheckInUseCase
from app.modules.estadias.application.use_cases.check_out import CheckOutUseCase

def get_estadia_repo() -> IEstadiaRepository:
    return EstadiaRepositoryImpl()

def get_crear_estadia_uc(repo=Depends(get_estadia_repo)):
    return CrearEstadiaUseCase(repo)

def get_check_in_uc(repo=Depends(get_estadia_repo)):
    return CheckInUseCase(repo)

def get_check_out_uc(repo=Depends(get_estadia_repo)):
    return CheckOutUseCase(repo)
