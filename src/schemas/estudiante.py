from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class EstudianteCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    programa: str = Field(min_length=1, max_length=120)
    semestre: int = Field(ge=1, le=14)


class EstudianteUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=120)
    programa: Optional[str] = Field(default=None, min_length=1, max_length=120)
    semestre: Optional[int] = Field(default=None, ge=1, le=14)


class EstudianteRead(BaseModel):
    id: UUID
    nombre: str
    programa: str
    semestre: int

    model_config = {"from_attributes": True}
