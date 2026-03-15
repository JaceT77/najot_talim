from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DEBUG: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_db_settings(self):
        if self.DATABASE_URL:
            return self

        missing = [
            name
            for name in ("DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT")
            if getattr(self, name) in (None, "")
        ]
        if missing:
            raise ValueError(
                f"Missing database settings: {', '.join(missing)}. "
                f"Set APP_DATABASE_URL or provide all APP_DB_* variables."
            )
        return self

    @property
    def database_url(self):
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix="APP_",
        extra="ignore",
    )

settings = Settings()  # type: ignore
