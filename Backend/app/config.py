from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    GEMINI_API_KEY: str
    CORS_ORIGINS: str
    UNIVERSITY_API_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()
