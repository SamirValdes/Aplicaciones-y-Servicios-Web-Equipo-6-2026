"""Módulo con las operaciones CRUD para la entidad persona"""

from sqlalchemy.orm import Session
from src.entities.persona import Persona
from src.schemas.persona import PersonaCreate, PersonaUpdate


def get_personas(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista paginada de personas de la base de datos"""
    return db.query(Persona).offset(skip).limit(limit).all()


def get_persona_by_id(db: Session, persona_id: int):
    """Busca y retorna una persona por su ID"""
    return db.query(Persona).filter(Persona.id == persona_id).first()


def get_persona_by_email(db: Session, email: str):
    """Busca y retorna una persona por su correo electronico"""
    return db.query(Persona).filter(Persona.email == email).first()


def create_persona(db: Session, persona: PersonaCreate):
    """Crea un nuevo registro de persona"""
    db_persona = Persona(**persona.model_dump())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona


def update_persona(db: Session, persona_id: int, persona_data: PersonaUpdate):
    """Actualiza los datos de una persona existente"""
    db_persona = get_persona_by_id(db, persona_id)
    if not db_persona:
        return None
    for key, value in persona_data.model_dump(exclude_unset=True).items():
        setattr(db_persona, key, value)
    db.commit()
    db.refresh(db_persona)
    return db_persona


def delete_persona(db: Session, persona_id: int):
    """Elimina una persona de la base de datos"""
    db_persona = get_persona_by_id(db, persona_id)
    if not db_persona:
        return None
    db.delete(db_persona)
    db.commit()
    return db_persona
