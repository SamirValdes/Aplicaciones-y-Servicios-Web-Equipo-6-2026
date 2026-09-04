from uuid import UUID, uuid4
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

# Asegúrate de que la ruta de importación coincida con tu proyecto
from src.database.database import Base


class Estudiante(Base):
    __tablename__ = "estudiantes"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    programa: Mapped[str] = mapped_column(String(120), nullable=False)
    semestre: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
