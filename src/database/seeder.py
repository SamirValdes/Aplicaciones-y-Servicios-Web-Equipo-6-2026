from sqlalchemy.orm import Session
from src.database.database import engine, Base
from src.entities.persona import Persona
from src.entities.estudiante import Estudiante
from src.entities.producto import Producto

def seed_data():
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
            print("? Seeder de Persona ejecutado con éxito.")
        else:
            print("? Los datos de Persona ya existen.")

if __name__ == "__main__":
    seed_data()
