"""
Application settings and configuration management.
"""

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_WORKERS: int = int(os.getenv("API_WORKERS", "4"))

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Mistral AI Configuration
    MISTRAL_API_KEY: str | None = os.getenv("MISTRAL_API_KEY")

    # Coral Configuration
    CORAL_SERVER_URL: str = os.getenv("CORAL_SERVER_URL", "http://localhost:8080")
    CORAL_API_KEY: str | None = os.getenv("CORAL_API_KEY")

    # Database Configuration
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")
    REDIS_URL: str | None = os.getenv("REDIS_URL")

    # Security
    JWT_SECRET_KEY: str | None = os.getenv("JWT_SECRET_KEY")
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:3001"
    ).split(",")

    # Email Configuration
    SMTP_HOST: str | None = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str | None = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str | None = os.getenv("SMTP_PASSWORD")

    # File Storage
    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "local")
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./storage")
    AWS_S3_BUCKET: str | None = os.getenv("AWS_S3_BUCKET")
    AWS_ACCESS_KEY_ID: str | None = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str | None = os.getenv("AWS_SECRET_ACCESS_KEY")

    # Monitoring
    SENTRY_DSN: str | None = os.getenv("SENTRY_DSN")
    ANALYTICS_ID: str | None = os.getenv("ANALYTICS_ID")

    @classmethod
    def validate(cls) -> None:
        """Validate required settings."""
        required_settings = [
            ("MISTRAL_API_KEY", cls.MISTRAL_API_KEY),
            ("CORAL_API_KEY", cls.CORAL_API_KEY),
        ]

        missing_settings = [
            name for name, value in required_settings if value is None or value == ""
        ]

        if missing_settings:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_settings)}"
            )

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENVIRONMENT.lower() == "production"

    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment."""
        return cls.ENVIRONMENT.lower() == "development"

    @classmethod
    def get_cors_origins(cls) -> list[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in cls.CORS_ORIGINS if origin.strip()]


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings
