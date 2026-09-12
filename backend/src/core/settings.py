from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str = Field(validation_alias=AliasChoices("PGPORT", "POSTGRES_PORT"))
    postgres_db: str
    redis_url: str = Field(
        default="redis://backend-redis:6379/0",
        validation_alias=AliasChoices("REDIS_URL", "CELERY_BROKER_URL"),
    )
    storage_dir: Path = Field(default_factory=lambda: BASE_DIR / "storage" / "files")

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
