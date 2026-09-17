"""Módulo de rutas (endpoints) para la API de estudiantes"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importamos el CRUD y los schemas de estudiante
from src.crud import estudiante as repo
from src.database.database import get_db
from src.schemas.estudiante import EstudianteCreate, EstudianteRead, EstudianteUpdate

# Ajustamos el prefijo y los tags para la documentación de Swagger
router = APIRouter(prefix="/estudiantes", tags=["estudiantes"])


@router.get("", response_model=list[EstudianteRead])
def listar_estudiantes(db: Session = Depends(get_db)):
    """Obtiene la lista de todos los estudiantes"""
    return repo.listar(db)


@router.get("/{estudiante_id}", response_model=EstudianteRead)
def obtener_estudiante(estudiante_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un estudiante especifico por su ID"""
    estudiante = repo.obtener_por_id(db, estudiante_id)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


@router.post(
    "",
    response_model=EstudianteRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_estudiante(datos: EstudianteCreate, db: Session = Depends(get_db)):
    """Crea un nuevo estudiante en la base de datos"""
    try:
        return repo.crear(db, datos)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.put("/{estudiante_id}", response_model=EstudianteRead)
def actualizar_estudiante(
    estudiante_id: UUID,
    datos: EstudianteUpdate,
    db: Session = Depends(get_db),
):
    """Actualiza los datos de un estudiante existente"""
    estudiante = repo.obtener_por_id(db, estudiante_id)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    try:
        return repo.actualizar(db, estudiante, datos)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/{estudiante_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante(estudiante_id: UUID, db: Session = Depends(get_db)):
    """Elimina un estudiante de la base de datos"""
    estudiante = repo.obtener_por_id(db, estudiante_id)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    repo.eliminar(db, estudiante)
