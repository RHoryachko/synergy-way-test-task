from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "development"
    
    class Config:
        env_file = ".env"


settings = Settings()
