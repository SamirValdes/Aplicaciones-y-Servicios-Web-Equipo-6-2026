"""Módulo que define los esquemas (schemas) para el estudiante"""

# 1. Librerías estándar
from typing import Optional
from uuid import UUID

# 2. Librerías de terceros
from pydantic import BaseModel, Field


class EstudianteCreate(BaseModel):
    """Esquema para la creacion de un nuevo estudiante"""

    nombre: str = Field(min_length=1, max_length=120)
    programa: str = Field(min_length=1, max_length=120)
    # Validamos que el semestre sea un número lógico para una universidad
    semestre: int = Field(ge=1, le=14)


class EstudianteUpdate(BaseModel):
    """Esquema para la actualizacion de datos de un estudiante"""

    # En las actualizaciones es buena práctica que los campos sean opcionales (Optional)
    # por si el usuario solo quiere actualizar un dato y no todos.
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=120)
    programa: Optional[str] = Field(default=None, min_length=1, max_length=120)
    semestre: Optional[int] = Field(default=None, ge=1, le=14)


class EstudianteRead(BaseModel):
    """Esquema para la lectura de datos de un estudiante"""

    id: UUID
    nombre: str
    programa: str
    semestre: int

    model_config = {"from_attributes": True}
