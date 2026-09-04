from contextlib import asynccontextmanager

from fastapi import FastAPI


from src.database.database import Base, engine


from src.api.estudiante import router as estudiantes_router
from src.api.producto import router as productos_router
from src.entities.estudiante import Estudiante
from src.entities.producto import Producto


@asynccontextmanager
async def lifespan(_app: FastAPI):

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Estudiantes - ITM 2026-2",
    description="API REST con FastAPI, SQLAlchemy y Neon PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API  - Aplicaciones y servicios web ITM 2026-2",
        "docs": "/docs",
    }


app.include_router(estudiantes_router)
app.include_router(productos_router)
