from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://localhost:5500/task_tracker"
    SECRET_KEY: str = Field(min_length=32, repr=False)
    TOKEN_ALGORITHM: Literal["HS256"] = "HS256"
    TOKEN_LIFETIME_MINUTES: int = Field(default=30, gt=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        hide_input_in_errors=True,
    )


# BaseSettings loads required fields from the environment or .env; the key has no code default.
settings = Settings()  # pyright: ignore[reportCallIssue]
