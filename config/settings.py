
"""
Centralized application configuration manager.

Loads environment variables, validates configuration,
and provides secure access to application settings.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic import AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application configuration and environment settings."""

    # Environment configuration
    app_name: str = "AI Backend Engineering Lab"

    app_env: Literal["development", "testing", "production"] = (
        "development"
    )

    debug: bool = True

    log_level: Literal[
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ] = "INFO"

    # AI provider configuration
    openrouter_api_key: SecretStr | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "OPENROUTER_API_KEY",
            "nvidia_api_key"
        )
    )

    openrouter_base_url: str = (
        "https://openrouter.ai/api/v1"
    )

    default_model: str = (
        "nvidia/nemotron-3-ultra-550b-a55b:free"
    )

    # Request configuration
    request_timeout: float = Field(
        default=60.0,
        gt=0,
        le=300
    )

    max_retries: int = Field(
        default=2,
        ge=0,
        le=5
    )

    # Database configuration
    database_url: SecretStr | None = None

    # Environment file configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def require_openrouter_api_key(self) -> str:
        """
        Return the API key or raise an error
        if it is not configured.
        """

        if self.openrouter_api_key is None:
            raise RuntimeError(
                "OPENROUTER_API_KEY is missing. "
                "Please configure it in your .env file."
            )

        return self.openrouter_api_key.get_secret_value()

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return a cached settings instance.

    Configuration is loaded only once during
    normal application execution.
    """

    return Settings()

def clear_settings_cache() -> None:
    """Clear cached settings, useful during testing."""

    get_settings.cache_clear()