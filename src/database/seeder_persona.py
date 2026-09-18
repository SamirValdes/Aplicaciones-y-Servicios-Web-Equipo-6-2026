"""Modulo para poblar la base de datos con datos iniciales de Persona."""
from sqlalchemy.orm import Session
from src.database.database import engine, Base
from src.entities.persona import Persona

def seed_data():
    """Crea las tablas e inserta el registro inicial de la entidad."""
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        if not session.query(Persona).first():
            print("Insertando datos iniciales de Persona...")
            nueva_persona = Persona(
                nombre="Vilmar",
                apellido="Rivas"
            )
            session.add(nueva_persona)
            session.commit()
            print("Seeder de Persona ejecutado con exito.")
        else:
            print("Los datos de Persona ya existen.")

if __name__ == "__main__":
    seed_data()
