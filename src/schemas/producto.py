from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProductoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    descripcion: Optional[str] = None
    precio: Decimal = Field(gt=0, decimal_places=2)
    stock: int = Field(ge=0)


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=120)
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = Field(default=None, gt=0, decimal_places=2)
    stock: Optional[int] = Field(default=None, ge=0)


class ProductoRead(BaseModel):
    id: UUID
    nombre: str
    descripcion: Optional[str]
    precio: Decimal
    stock: int

    model_config = {"from_attributes": True}