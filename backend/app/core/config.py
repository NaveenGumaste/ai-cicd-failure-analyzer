
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Locate the project root directory.
# config.py -> core -> app -> backend -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """
    Centralized application configuration.

    Values are loaded from the project's .env file
    and validated using Pydantic.
    """

    app_name: str = "AI CI/CD Failure Analyzer"
    app_version: str = "1.0.0"
    app_env: str = "development"

    api_v1_prefix: str = "/api/v1"

    database_url: str

    cors_origins: str = (
        "http://localhost:3000,"
        "http://127.0.0.1:3000"
    )

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def allowed_origins(self) -> list[str]:
        """Convert comma-separated origins into a list."""

        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


# Create a reusable settings instance.
settings = Settings()
