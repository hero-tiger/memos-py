from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Memos"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    HOST: str = "0.0.0.0"
    PORT: int = 8081
    
    DATA_DIR: str = "./data"
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/memos.db"
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    SMTP_FROM_NAME: str = "Memos"
    SMTP_USE_TLS: bool = True
    
    S3_BUCKET: Optional[str] = None
    S3_REGION: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_ENDPOINT: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
