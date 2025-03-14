# app/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:Tusdatos**@localhost/eventos_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu_clave_secreta")  # Asegúrate de que esto esté anotado
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"  # Cargar variables de entorno desde un archivo .env

settings = Settings()