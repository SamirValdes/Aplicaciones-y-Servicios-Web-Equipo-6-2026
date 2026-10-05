"""Pruebas de los endpoints de productos usando una base SQLite desechable."""

import os
from collections.abc import Generator
from decimal import Decimal

os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from src.database.database import Base, get_db
from src.entities.producto import Producto

engine_test = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
sesion_prueba = sessionmaker(
    bind=engine_test,
    autoflush=False,
    autocommit=False,
)


def override_get_db() -> Generator[Session, None, None]:
    """Provee una sesión aislada para cada prueba."""
    db = sesion_prueba()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def cliente() -> Generator[TestClient, None, None]:
    """Inicia la API con tablas SQLite nuevas y elimina overrides al finalizar."""
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app, raise_server_exceptions=False) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def insertar_producto() -> str:
    """Crea un producto directamente para preparar una prueba de lectura."""
    db = sesion_prueba()
    try:
        producto = Producto(
            nombre="Producto de prueba",
            descripcion="Registro preparado para la prueba",
            precio=Decimal("12.50"),
            stock=6,
        )
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return str(producto.id)
    finally:
        db.close()


def test_listar_productos_devuelve_lista(cliente: TestClient) -> None:
    producto_id = insertar_producto()

    respuesta = cliente.get("/productos")

    assert respuesta.status_code == 200
    assert respuesta.json() == [
        {
            "id": producto_id,
            "nombre": "Producto de prueba",
            "descripcion": "Registro preparado para la prueba",
            "precio": "12.50",
            "stock": 6,
        }
    ]


def test_listar_productos_devuelve_500_si_falla_base_datos(
    cliente: TestClient,
) -> None:
    def base_datos_no_disponible():
        raise RuntimeError("Base de datos no disponible")

    app.dependency_overrides[get_db] = base_datos_no_disponible

    respuesta = cliente.get("/productos")

    assert respuesta.status_code == 500
    assert respuesta.text == "Internal Server Error"


def test_obtener_producto_por_id_devuelve_registro(cliente: TestClient) -> None:
    producto_id = insertar_producto()

    respuesta = cliente.get(f"/productos/{producto_id}")

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "id": producto_id,
        "nombre": "Producto de prueba",
        "descripcion": "Registro preparado para la prueba",
        "precio": "12.50",
        "stock": 6,
    }


def test_obtener_producto_inexistente_devuelve_404(cliente: TestClient) -> None:
    respuesta = cliente.get("/productos/00000000-0000-0000-0000-000000000001")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Producto no encontrado"}


def test_crear_producto_devuelve_201_y_registro(cliente: TestClient) -> None:
    datos = {
        "nombre": "Producto nuevo",
        "descripcion": "Creado desde la prueba",
        "precio": 25.75,
        "stock": 4,
    }

    respuesta = cliente.post("/productos", json=datos)

    assert respuesta.status_code == 201
    assert respuesta.json()["id"]
    assert respuesta.json()["nombre"] == datos["nombre"]
    assert respuesta.json()["descripcion"] == datos["descripcion"]
    assert respuesta.json()["precio"] == "25.75"
    assert respuesta.json()["stock"] == datos["stock"]


def test_crear_producto_con_datos_invalidos_devuelve_422(
    cliente: TestClient,
) -> None:
    respuesta = cliente.post(
        "/productos",
        json={"nombre": "", "precio": -4, "stock": "sin inventario"},
    )

    assert respuesta.status_code == 422
    assert isinstance(respuesta.json()["detail"], list)
    assert respuesta.json()["detail"]


def test_actualizar_producto_existente_devuelve_cambios(
    cliente: TestClient,
) -> None:
    producto_id = insertar_producto()

    respuesta = cliente.put(
        f"/productos/{producto_id}",
        json={"stock": 10},
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == producto_id
    assert respuesta.json()["nombre"] == "Producto de prueba"
    assert respuesta.json()["stock"] == 10


def test_actualizar_producto_inexistente_devuelve_404(
    cliente: TestClient,
) -> None:
    respuesta = cliente.put(
        "/productos/00000000-0000-0000-0000-000000000001",
        json={"stock": 10},
    )

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Producto no encontrado"}


def test_eliminar_producto_existente_devuelve_204(cliente: TestClient) -> None:
    producto_id = insertar_producto()

    respuesta = cliente.delete(f"/productos/{producto_id}")

    assert respuesta.status_code == 204
    assert respuesta.content == b""
    assert cliente.get(f"/productos/{producto_id}").status_code == 404


def test_eliminar_producto_inexistente_devuelve_404(cliente: TestClient) -> None:
    respuesta = cliente.delete("/productos/00000000-0000-0000-0000-000000000001")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Producto no encontrado"}
