from sqlalchemy.orm import Session
from src.entities.persona import Persona
from src.schemas.persona import PersonaCreate, PersonaUpdate

def get_personas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Persona).offset(skip).limit(limit).all()

def get_persona_by_id(db: Session, persona_id: int):
    return db.query(Persona).filter(Persona.id == persona_id).first()

def get_persona_by_email(db: Session, email: str):
    return db.query(Persona).filter(Persona.email == email).first()

def create_persona(db: Session, persona: PersonaCreate):
    db_persona = Persona(**persona.model_dump())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

def update_persona(db: Session, persona_id: int, persona_data: PersonaUpdate):
    db_persona = get_persona_by_id(db, persona_id)
    if not db_persona:
        return None
    for key, value in persona_data.model_dump(exclude_unset=True).items():
        setattr(db_persona, key, value)
    db.commit()
    db.refresh(db_persona)
    return db_persona

def delete_persona(db: Session, persona_id: int):
    db_persona = get_persona_by_id(db, persona_id)
    if not db_persona:
        return None
    db.delete(db_persona)
    db.commit()
    return db_persona
