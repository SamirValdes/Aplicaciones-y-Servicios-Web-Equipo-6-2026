from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.producto import Producto
from src.schemas.producto import ProductoCreate, ProductoUpdate


def listar(db: Session) -> list[Producto]:
    return list(db.scalars(select(Producto).order_by(Producto.nombre)))


def obtener_por_id(db: Session, producto_id: UUID) -> Producto | None:
    return db.get(Producto, producto_id)


def crear(db: Session, datos: ProductoCreate) -> Producto:
    producto = Producto(
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        precio=datos.precio,
        stock=datos.stock,
    )
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def actualizar(db: Session, producto: Producto, datos: ProductoUpdate) -> Producto:
    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(producto, campo, valor)

    db.commit()
    db.refresh(producto)
    return producto


def eliminar(db: Session, producto: Producto) -> None:
    db.delete(producto)
    db.commit()