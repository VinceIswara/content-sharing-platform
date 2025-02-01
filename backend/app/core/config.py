from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Config
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Content Sharing Platform"
    
    # Supabase Config
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Security
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 