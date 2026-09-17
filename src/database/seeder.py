"""Script para poblar la base de datos con datos iniciales"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.database import Base, SessionLocal, engine
from src.entities.estudiante import Estudiante

ESTUDIANTES_SEMILLA = [
    {"nombre": "Juan David Perez", "programa": "Ingenieria de Sistemas", "semestre": 5},
    {
        "nombre": "Maria Camila Lopez",
        "programa": "Tecnologia en Desarrollo de Software",
        "semestre": 3,
    },
    {"nombre": "Andres Felipe Ruiz", "programa": "Ingenieria Biomedica", "semestre": 8},
]


def crear_tablas() -> None:
    """Crea las tablas en la base de datos que aun no existen"""
    Base.metadata.create_all(bind=engine)
    print("Tablas verificadas/creadas")


def _insertar_si_falta(
    db: Session,
    modelo: type,
    campo: str,
    filas: list[dict],
) -> int:
    """Inserta registros en la base de datos si no existen previamente"""
    insertadas = 0
    columna = getattr(modelo, campo)

    for datos in filas:
        etiqueta = datos[campo]
        existe = db.scalar(select(modelo).where(columna == etiqueta))
        if existe is not None:
            print(f"Ya existe: {etiqueta}")
            continue

        db.add(modelo(**datos))
        insertadas += 1
        print(f"Insertada: {etiqueta}")

    db.commit()
    return insertadas


def main() -> None:
    """Funcion principal que ejecuta la creacion de tablas y la siembra de datos"""
    crear_tablas()

    db = SessionLocal()
    try:
        estudiantes = _insertar_si_falta(db, Estudiante, "nombre", ESTUDIANTES_SEMILLA)
    finally:
        db.close()

    print(f"Seeder terminado. Estudiantes nuevos: {estudiantes}")


if __name__ == "__main__":
    main()
