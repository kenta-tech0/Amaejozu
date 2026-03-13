"""
Application configuration management
環境変数とアプリケーション設定を管理
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Database
    DATABASE_URL: str = "mysql+aiomysql://app_user:app_password@db:3306/speaking_practice_db"

    # Anthropic Claude API
    ANTHROPIC_API_KEY: str = ""

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # Application
    APP_NAME: str = "SpeakEasy - English Speaking Practice"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
