"""Runtime settings for the chat API."""

from functools import cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import DEFAULT_MODEL, MODEL_PRICES


class Settings(BaseSettings):
    """Settings read from CHAT_* environment variables."""

    model_config = SettingsConfigDict(env_prefix="CHAT_")

    table_name: str
    anthropic_key_param: str
    ip_salt_param: str
    notes_bucket: str
    notes_key: str = "notes.md"
    profile_url: str = "https://adammichaelspaulding.com/profile.json"
    model: str = DEFAULT_MODEL
    monthly_budget_usd: float = 4.50
    rate_limit_per_10_min: int = 10
    rate_limit_per_day: int = 30

    @field_validator("model")
    @classmethod
    def check_model_has_prices(cls, value: str) -> str:
        if value not in MODEL_PRICES:
            raise ValueError(f"No prices configured for model {value}")
        return value


@cache
def get_settings() -> Settings:
    """Return the settings, read once per process."""
    return Settings()
