"""Módulo de configuración de variables de entorno y conexión."""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)


class Settings(BaseSettings):
    """Define las configuraciones y variables de entorno del proyecto."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str

    @property
    def sqlalchemy_url(self) -> str:
        """Formatea la URL para usar el driver psycopg."""
        if self.database_url.startswith("postgresql://"):
            return self.database_url.replace(
                "postgresql://", "postgresql+psycopg://", 1
            )
        return self.database_url


settings = Settings()
