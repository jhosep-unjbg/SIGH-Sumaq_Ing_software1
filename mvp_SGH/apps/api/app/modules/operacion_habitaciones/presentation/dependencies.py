from fastapi import Depends
from app.modules.operacion_habitaciones.domain.repositories.tarea_repository import ITareaRepository
from app.modules.operacion_habitaciones.infrastructure.repositories.tarea_repository_impl import TareaRepositoryImpl
from app.modules.operacion_habitaciones.application.use_cases.crear_tarea import CrearTareaUseCase
from app.modules.operacion_habitaciones.application.use_cases.completar_tarea import CompletarTareaUseCase

def get_tarea_repo() -> ITareaRepository:
    return TareaRepositoryImpl()
def get_crear_tarea_uc(repo=Depends(get_tarea_repo)):
    return CrearTareaUseCase(repo)
def get_completar_tarea_uc(repo=Depends(get_tarea_repo)):
    return CompletarTareaUseCase(repo)
