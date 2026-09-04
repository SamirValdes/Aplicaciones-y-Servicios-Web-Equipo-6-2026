from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

# Asegúrate de que las rutas de importación coincidan con la estructura de tu proyecto
from src.entities.estudiante import Estudiante
from src.schemas.estudiante import EstudianteCreate, EstudianteUpdate


def listar(db: Session) -> list[Estudiante]:
    return list(db.scalars(select(Estudiante).order_by(Estudiante.nombre)))


def obtener_por_id(db: Session, estudiante_id: UUID) -> Estudiante | None:
    return db.get(Estudiante, estudiante_id)


def crear(db: Session, datos: EstudianteCreate) -> Estudiante:
    estudiante = Estudiante(
        nombre=datos.nombre,
        programa=datos.programa,
        semestre=datos.semestre,
    )
    db.add(estudiante)
    db.commit()
    db.refresh(estudiante)
    return estudiante


def actualizar(
    db: Session, estudiante: Estudiante, datos: EstudianteUpdate
) -> Estudiante:
    # Como en el schema de Update definimos los campos como opcionales (Optional),
    # validamos que vengan datos antes de sobrescribirlos.
    if datos.nombre is not None:
        estudiante.nombre = datos.nombre
    if datos.programa is not None:
        estudiante.programa = datos.programa
    if datos.semestre is not None:
        estudiante.semestre = datos.semestre

    db.commit()
    db.refresh(estudiante)
    return estudiante


def eliminar(db: Session, estudiante: Estudiante) -> None:
    db.delete(estudiante)
    db.commit()
