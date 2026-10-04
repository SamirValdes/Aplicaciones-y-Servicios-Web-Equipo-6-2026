"""Módulo que define el modelo de base de datos para producto"""

from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


# pylint: disable=too-few-public-methods
class Producto(Base):
    """Clase que representa la entidad de producto en la base de datos"""

    __tablename__ = "productos"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
