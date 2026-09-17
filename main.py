"""Módulo principal de la aplicación FastAPI"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.database import Base, engine

# Importación de routers de cada módulo
from src.api.estudiante import router as estudiantes_router
from src.api.producto import router as productos_router
from src.api.persona import router as personas_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Manejador del ciclo de vida para inicializar la base de datos"""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Equipo 6 - ITM 2026-2",
    description="API REST con FastAPI, SQLAlchemy y Neon PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)

# Registro de routers
app.include_router(estudiantes_router)
app.include_router(productos_router)
app.include_router(personas_router)


@app.get("/")
def inicio():
    """Endpoint raiz que retorna la informacion basica de la API"""
    return {
        "mensaje": "API - Aplicaciones y servicios web ITM 2026-2",
        "docs": "/docs",
    }
