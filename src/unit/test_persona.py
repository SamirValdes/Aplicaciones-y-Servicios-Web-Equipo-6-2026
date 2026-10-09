"""Pruebas unitarias para la API de Personas"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.database import Base, get_db
from main import app
from src.entities.persona import Persona

# --- Configuración de Base de Datos en Memoria (SQLite) para Pruebas ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Reemplazamos la conexión real por la de prueba
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Fixture para crear las tablas antes de las pruebas y borrarlas al final
@pytest.fixture(autouse=True)
def run_around_tests():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# --- DATOS DE PRUEBA ---
PERSONA_DATA_VALIDA = {
    "nombre": "Vilmar Rivas Test",
    "email": "vilmar.test@email.com",
    "telefono": "3001234567",
    "activo": True
}

PERSONA_DATA_INCOMPLETA = {
    "nombre": "Falta Correo"
}

# --- 1. PRUEBAS PARA POST (Crear) ---
def test_create_persona_normal():
    """Prueba normal: Crear una persona con datos válidos."""
    response = client.post("/personas/", json=PERSONA_DATA_VALIDA)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == PERSONA_DATA_VALIDA["nombre"]
    assert data["email"] == PERSONA_DATA_VALIDA["email"]
    assert "id" in data

def test_create_persona_error_duplicado():
    """Prueba de error: Crear persona con correo que ya existe."""
    # Insertar la primera vez
    client.post("/personas/", json=PERSONA_DATA_VALIDA)
    # Intentar insertar la misma
    response = client.post("/personas/", json=PERSONA_DATA_VALIDA)
    assert response.status_code == 400
    assert response.json()["detail"] == "El correo ya existe"

def test_create_persona_error_datos_incompletos():
    """Prueba de error: Faltan campos obligatorios."""
    response = client.post("/personas/", json=PERSONA_DATA_INCOMPLETA)
    assert response.status_code == 422 # Error de validación (Unprocessable Entity)

# --- 2. PRUEBAS PARA GET (Obtener lista) ---
def test_read_personas_normal():
    """Prueba normal: Obtener la lista de personas."""
    # Insertar una para que no esté vacía
    client.post("/personas/", json=PERSONA_DATA_VALIDA)
    response = client.get("/personas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# (Como FastAPI maneja la paginación internamente, el error más común es mandar un string en vez de un int)
def test_read_personas_error_tipo_dato():
    """Prueba de error: Enviar un tipo de dato incorrecto en skip."""
    response = client.get("/personas/?skip=letras")
    assert response.status_code == 422

# --- 3. PRUEBAS PARA GET POR ID ---
def test_read_persona_normal():
    """Prueba normal: Obtener una persona por su ID válido."""
    create_response = client.post("/personas/", json=PERSONA_DATA_VALIDA)
    persona_id = create_response.json()["id"]
    
    response = client.get(f"/personas/{persona_id}")
    assert response.status_code == 200
    assert response.json()["id"] == persona_id

def test_read_persona_error_no_existe():
    """Prueba de error: Obtener una persona con ID inexistente."""
    response = client.get("/personas/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Persona no encontrada"

# --- 4. PRUEBAS PARA PUT (Actualizar) ---
def test_update_persona_normal():
    """Prueba normal: Actualizar datos de una persona existente."""
    create_response = client.post("/personas/", json=PERSONA_DATA_VALIDA)
    persona_id = create_response.json()["id"]
    
    datos_actualizados = {
        "nombre": "Vilmar Modificado",
        "email": "vilmar.test@email.com", # Asumimos que no lo cambia
        "telefono": "3009999999",
        "activo": False
    }
    response = client.put(f"/personas/{persona_id}", json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Vilmar Modificado"

def test_update_persona_error_no_existe():
    """Prueba de error: Actualizar una persona con ID inexistente."""
    datos_actualizados = {
        "nombre": "No Existe",
        "email": "no@existe.com",
        "telefono": "123",
        "activo": True
    }
    response = client.put("/personas/9999", json=datos_actualizados)
    assert response.status_code == 404
    assert response.json()["detail"] == "Persona no encontrada"

# --- 5. PRUEBAS PARA DELETE (Eliminar) ---
def test_delete_persona_normal():
    """Prueba normal: Eliminar una persona existente."""
    create_response = client.post("/personas/", json=PERSONA_DATA_VALIDA)
    persona_id = create_response.json()["id"]
    
    response = client.delete(f"/personas/{persona_id}")
    assert response.status_code == 204 # No Content

def test_delete_persona_error_no_existe():
    """Prueba de error: Eliminar una persona con ID inexistente."""
    response = client.delete("/personas/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Persona no encontrada"

