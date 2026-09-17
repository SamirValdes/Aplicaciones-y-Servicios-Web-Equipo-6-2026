"""Módulo para la inicialización y sesión de la base de datos"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.database.config import settings

engine = create_engine(settings.sqlalchemy_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# pylint: disable=too-few-public-methods
class Base(DeclarativeBase):
    """Clase base declarativa para los modelos de SQLAlchemy"""


def get_db() -> Generator[Session, None, None]:
    """Genera y gestiona las sesiones de conexion a la base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
