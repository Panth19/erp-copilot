"""
Centralized settings, read from environment variables with safe dev defaults.
In production, JWT_SECRET_KEY must be overridden via a real .env file.
"""
import os


class Settings:
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "dev-only-insecure-secret-change-me")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    # Cookie
    COOKIE_NAME: str = "access_token"
    COOKIE_SECURE: bool = os.getenv("COOKIE_SECURE", "false").lower() == "true"

    # Data paths (relative to backend/, data lives one level up)
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

    # CORS -- allow the React dev server
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]


settings = Settings()
