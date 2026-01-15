import os

from pydantic_settings import BaseSettings
from pydantic import Field


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

class Settings(BaseSettings):
    database_url: str = Field(default=f"postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}")
    redis_url: str = "redis://localhost:6379/0"
    jsonplaceholder_url: str = "https://jsonplaceholder.typicode.com"
    dummyjson_url: str = "https://dummyjson.com"
    env: str = "development"
    
    class Config:
        env_file = ".env"


settings = Settings()
