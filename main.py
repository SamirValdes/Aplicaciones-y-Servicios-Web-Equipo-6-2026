from fastapi import FastAPI
from src.database.database import Base, engine
from src.api.estudiante import router as estudiante_router
from src.api.persona import router as persona_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Equipo 6")

app.include_router(estudiante_router)
app.include_router(persona_router)

@app.get("/")
def read_root():
    return {"message": "API activa"}
