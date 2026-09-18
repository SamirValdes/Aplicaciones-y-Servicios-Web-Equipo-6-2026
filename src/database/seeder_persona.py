"""Script para poblar la base de datos con datos iniciales."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.database import Base, SessionLocal, engine
from src.entities.persona import Persona

PERSONAS_SEMILLA = [
    {
        "nombre": "Vilmar Rivas",
        "email": "vilmar.rivas@email.com",
        "telefono": "3000000000",
        "activo": True,
    }
]

def crear_tablas() -> None:
    """Crea las tablas en la base de datos que aun no existen."""
    Base.metadata.create_all(bind=engine)
    print("Tablas verificadas/creadas")

def _insertar_si_falta(
    db: Session,
    modelo: type,
    campo: str,
    filas: list[dict],
) -> int:
    """Inserta registros en la base de datos si no existen previamente."""
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
    """Funcion principal que ejecuta la creacion de tablas y la siembra de datos."""
    crear_tablas()

    db = SessionLocal()
    try:
        personas = _insertar_si_falta(db, Persona, "email", PERSONAS_SEMILLA)
    finally:
        db.close()

    print(f"Seeder terminado. Personas nuevas: {personas}")

if __name__ == "__main__":
    main()
