"""Módulo que define el modelo de base de datos para estudiante"""

from uuid import UUID, uuid4
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


from src.database.database import Base


# pylint: disable=too-few-public-methods
class Estudiante(Base):
    """Clase que representa la entidad de estudiante en la base de datos"""

    __tablename__ = "estudiantes"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    programa: Mapped[str] = mapped_column(String(120), nullable=False)
    semestre: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
