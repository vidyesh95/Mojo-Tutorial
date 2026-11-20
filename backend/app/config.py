# backend/app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_PATH: str = "backend/app.db"
    BETTER_AUTH_SECRET: str = "super-secret-random-32-byte-hex-key-change-me"
    SESSION_COOKIE_NAME: str = "better-auth.session_token"
    SESSION_MAX_AGE_DAYS: int = 7
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
