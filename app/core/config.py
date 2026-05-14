from dataclasses import dataclass, field
from os import getenv


def _csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    """Application settings with safe defaults for local development."""

    app_name: str = getenv("APP_NAME", "TaskFlow API")
    environment: str = getenv("ENVIRONMENT", "development")
    api_v1_prefix: str = getenv("API_V1_PREFIX", "/api/v1")
    log_level: str = getenv("LOG_LEVEL", "INFO")
    cors_origins: list[str] = field(default_factory=lambda: _csv(getenv("CORS_ORIGINS", "*")))
    rate_limit_requests: int = int(getenv("RATE_LIMIT_REQUESTS", "60"))
    rate_limit_window_seconds: int = int(getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))



settings = Settings()
