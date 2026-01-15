from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://synergy:synergy123@db:5432/synergy_db"
    redis_url: str = "redis://redis:6379/0"
    jsonplaceholder_url: str = "https://jsonplaceholder.typicode.com"
    dummyjson_url: str = "https://dummyjson.com"
    env: str = "development"
    
    class Config:
        env_file = ".env"


settings = Settings()
