"""Módulo que define el modelo de base de datos para persona"""

from sqlalchemy import Column, Integer, String, Boolean
from src.database.database import Base


# pylint: disable=too-few-public-methods
class Persona(Base):
    """Clase que representa la entidad de persona en la base de datos"""

    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    telefono = Column(String, nullable=True)
    activo = Column(Boolean, default=True)
