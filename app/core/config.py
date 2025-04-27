"""Application settings and configuration."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from urllib.parse import urlparse

from dotenv import load_dotenv


@dataclass
class Settings:
    """Application settings."""

    # Application settings
    DEBUG: bool = False
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret")

    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "").lower() == "true"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")

    # CORS settings
    CORS_ORIGINS: List[str] = field(
        default_factory=lambda: os.getenv("CORS_ORIGINS", "*").split(",")
    )
    CORS_METHODS: List[str] = field(
        default_factory=lambda: os.getenv("CORS_METHODS", "*").split(",")
    )
    CORS_HEADERS: List[str] = field(
        default_factory=lambda: os.getenv("CORS_HEADERS", "*").split(",")
    )
    CORS_CREDENTIALS: bool = os.getenv("CORS_CREDENTIALS", "True").lower() == "true"

    # API settings
    API_V1_PREFIX: str = os.getenv("API_V1_PREFIX", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Backend API")

    # File storage settings
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", "uploads"))
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "5242880"))  # 5MB

    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv(
        "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    def __post_init__(self):
        """Validate settings after initialization."""
        # Validate DATABASE_URL
        try:
            parsed = urlparse(self.DATABASE_URL)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError("Invalid DATABASE_URL format")
        except Exception as e:
            raise ValueError(f"Invalid DATABASE_URL: {e}")

        # Ensure SECRET_KEY is set
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set")

        # Create UPLOAD_DIR if it doesn't exist
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


load_dotenv()
# Load settings from environment
settings = Settings()
