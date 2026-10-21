
"""Application settings loaded from environment variables."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./tableturn.db"
    seed_dir: str = "seed"
    default_quote_minutes: int = 40
    host: str = "0.0.0.0"
    port: int = Field(default=8080, ge=1, le=65535)
