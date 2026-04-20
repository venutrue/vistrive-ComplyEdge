from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ComplyEdge API"
    app_env: str = Field(default="dev", pattern="^(dev|staging|prod|test)$")
    debug: bool = True

    api_prefix: str = "/api/v1"
    database_url_override: str | None = Field(default=None, alias="DATABASE_URL")
    app_env: str = Field(default="dev", pattern="^(dev|staging|prod)$")
    debug: bool = True

    api_prefix: str = "/api/v1"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "complyedge"
    postgres_password: str = "complyedge"
    postgres_db: str = "complyedge"

    redis_url: str = "redis://localhost:6379/0"
    auth_secret_key: str = "change-me-in-production"
    mfa_static_otp: str = "123456"
    access_token_minutes: int = 60
    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", populate_by_name=True)

    @property
    def database_url(self) -> str:
        if self.database_url_override:
            return self.database_url_override

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
