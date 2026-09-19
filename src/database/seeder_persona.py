"""Script para poblar la base de datos con datos iniciales de personas."""

from src.database.database import SessionLocal
from src.entities.persona import Persona
from src.database.seeder import crear_tablas, _insertar_si_falta

PERSONAS_SEMILLA = [
    {
        "nombre": "Vilmar Rivas",
        "email": "vilmar.rivas@email.com",
        "telefono": "3000000000",
        "activo": True,
    }
]

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
