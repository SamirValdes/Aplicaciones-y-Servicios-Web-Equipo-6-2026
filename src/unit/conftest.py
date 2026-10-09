import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from src.database.database import Base, get_db

# 1. Configura SQLite en memoria compartiendo la conexión entre hilos (StaticPool)
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Reemplaza la BD real por la BD de pruebas
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    # 3. Crea las tablas antes de cada prueba
    Base.metadata.create_all(bind=engine)
    yield
    # 4. Borra las tablas al terminar
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def cliente():
    # 5. Centraliza el cliente de pruebas aquí
    return TestClient(app)