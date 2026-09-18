from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud import producto as repo
from src.database.database import get_db
from src.schemas.producto import ProductoCreate, ProductoRead, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("", response_model=list[ProductoRead])
def listar_productos(db: Session = Depends(get_db)):
    return repo.listar(db)


@router.get("/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: UUID, db: Session = Depends(get_db)):
    producto = repo.obtener_por_id(db, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post(
    "",
    response_model=ProductoRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_producto(datos: ProductoCreate, db: Session = Depends(get_db)):
    return repo.crear(db, datos)


@router.put("/{producto_id}", response_model=ProductoRead)
def actualizar_producto(
    producto_id: UUID,
    datos: ProductoUpdate,
    db: Session = Depends(get_db),
):
    producto = repo.obtener_por_id(db, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return repo.actualizar(db, producto, datos)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: UUID, db: Session = Depends(get_db)):
    producto = repo.obtener_por_id(db, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    repo.eliminar(db, producto)