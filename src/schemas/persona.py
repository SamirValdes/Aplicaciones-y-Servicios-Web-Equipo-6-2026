"""Módulo que define los esquemas (schemas) para la persona"""

# 1. Librerías estándar
from typing import Optional

# 2. Librerías de terceros
from pydantic import BaseModel, EmailStr, Field


class PersonaBase(BaseModel):
    """Esquema base con los atributos comunes de persona"""

    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    activo: bool = True


class PersonaCreate(PersonaBase):
    """Esquema para la creacion de una nueva persona"""


class PersonaUpdate(BaseModel):
    """Esquema para la actualizacion de datos de una persona"""

    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = None


class PersonaResponse(PersonaBase):
    """Esquema de respuesta para la lectura de una persona"""

    id: int

    # pylint: disable=too-few-public-methods
    class Config:
        """Configuracion de Pydantic para mapear atributos del ORM"""

        from_attributes = True
