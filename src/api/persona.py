from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.persona import PersonaCreate, PersonaUpdate, PersonaResponse
from src.crud import persona as crud_persona

router = APIRouter(prefix="/personas", tags=["Personas"])

@router.get("/", response_model=List[PersonaResponse])
def read_personas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_persona.get_personas(db, skip=skip, limit=limit)

@router.post("/", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    db_persona = crud_persona.get_persona_by_email(db, email=persona.email)
    if db_persona:
        raise HTTPException(status_code=400, detail="El correo ya existe")
    return crud_persona.create_persona(db, persona)

@router.get("/{persona_id}", response_model=PersonaResponse)
def read_persona(persona_id: int, db: Session = Depends(get_db)):
    db_persona = crud_persona.get_persona_by_id(db, persona_id)
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return db_persona

@router.put("/{persona_id}", response_model=PersonaResponse)
def update_persona(persona_id: int, persona: PersonaUpdate, db: Session = Depends(get_db)):
    updated_persona = crud_persona.update_persona(db, persona_id, persona)
    if not updated_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return updated_persona

@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    deleted = crud_persona.delete_persona(db, persona_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return None
