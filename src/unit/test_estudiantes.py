import pytest
from http import HTTPStatus
from uuid import uuid4
from fastapi.testclient import TestClient

from main import app

ESTUDIANTE_VALIDO = {
    "nombre": "Carlos Perez",
    "programa": "Ingenieria de Software",
    "semestre": 3,
}

ESTUDIANTE_ACTUALIZADO = {
    "nombre": "Carlos Alberto Perez",
    "programa": "Desarrollo Web",
    "semestre": 4,
}




def _crear_estudiante(cliente, datos=None):
    respuesta = cliente.post("/estudiantes", json=datos or ESTUDIANTE_VALIDO)
    assert respuesta.status_code == HTTPStatus.CREATED.value
    return respuesta.json()


def test_listar_estudiantes_devuelve_200_y_una_lista(cliente):
    _crear_estudiante(cliente)
    respuesta = cliente.get("/estudiantes")

    assert respuesta.status_code == HTTPStatus.OK.value
    cuerpo = respuesta.json()
    assert isinstance(cuerpo, list)
    assert len(cuerpo) >= 1
    nombres = [est["nombre"] for est in cuerpo]
    assert ESTUDIANTE_VALIDO["nombre"] in nombres


def test_listar_estudiantes_vacio_devuelve_200_y_lista_vacia(cliente):
    respuesta = cliente.get("/estudiantes")

    assert respuesta.status_code == HTTPStatus.OK.value
    assert isinstance(respuesta.json(), list)


def test_obtener_estudiante_devuelve_200(cliente):
    creada = _crear_estudiante(cliente)
    respuesta = cliente.get(f"/estudiantes/{creada['id']}")

    assert respuesta.status_code == HTTPStatus.OK.value
    cuerpo = respuesta.json()
    assert cuerpo["id"] == creada["id"]
    assert cuerpo["nombre"] == ESTUDIANTE_VALIDO["nombre"]
    assert cuerpo["programa"] == ESTUDIANTE_VALIDO["programa"]
    assert cuerpo["semestre"] == ESTUDIANTE_VALIDO["semestre"]


def test_obtener_estudiante_inexistente_devuelve_404(cliente):
    respuesta = cliente.get(f"/estudiantes/{uuid4()}")

    assert respuesta.status_code == HTTPStatus.NOT_FOUND.value
    assert respuesta.json()["detail"] == "Estudiante no encontrado"


def test_crear_estudiante_devuelve_201(cliente):
    respuesta = cliente.post("/estudiantes", json=ESTUDIANTE_VALIDO)

    assert respuesta.status_code == HTTPStatus.CREATED.value
    cuerpo = respuesta.json()
    assert "id" in cuerpo
    assert cuerpo["nombre"] == ESTUDIANTE_VALIDO["nombre"]
    assert cuerpo["programa"] == ESTUDIANTE_VALIDO["programa"]
    assert cuerpo["semestre"] == ESTUDIANTE_VALIDO["semestre"]


def test_crear_estudiante_con_nombre_vacio_devuelve_422(cliente):
    respuesta = cliente.post(
        "/estudiantes",
        json={"nombre": "", "programa": "Ingenieria de Software", "semestre": 3},
    )

    assert respuesta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value


def test_actualizar_estudiante_devuelve_200(cliente):
    creada = _crear_estudiante(cliente)
    respuesta = cliente.put(
        f"/estudiantes/{creada['id']}",
        json=ESTUDIANTE_ACTUALIZADO,
    )

    assert respuesta.status_code == HTTPStatus.OK.value
    cuerpo = respuesta.json()
    assert cuerpo["id"] == creada["id"]
    assert cuerpo["nombre"] == ESTUDIANTE_ACTUALIZADO["nombre"]
    assert cuerpo["programa"] == ESTUDIANTE_ACTUALIZADO["programa"]
    assert cuerpo["semestre"] == ESTUDIANTE_ACTUALIZADO["semestre"]


def test_actualizar_estudiante_inexistente_devuelve_404(cliente):
    respuesta = cliente.put(f"/estudiantes/{uuid4()}", json=ESTUDIANTE_ACTUALIZADO)

    assert respuesta.status_code == HTTPStatus.NOT_FOUND.value
    assert respuesta.json()["detail"] == "Estudiante no encontrado"


def test_borrar_estudiante_creado_devuelve_204(cliente):
    creada = _crear_estudiante(cliente)

    respuesta = cliente.delete(f"/estudiantes/{creada['id']}")

    assert respuesta.status_code == HTTPStatus.NO_CONTENT.value
    consulta = cliente.get(f"/estudiantes/{creada['id']}")
    assert consulta.status_code == HTTPStatus.NOT_FOUND.value


def test_borrar_estudiante_inexistente_devuelve_404(cliente):
    respuesta = cliente.delete(f"/estudiantes/{uuid4()}")

    assert respuesta.status_code == HTTPStatus.NOT_FOUND.value
    assert respuesta.json()["detail"] == "Estudiante no encontrado"
