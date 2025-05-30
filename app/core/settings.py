from typing import Literal

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl

from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../env",        
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "moretti-customer"
    POSTGRES_PASSWORD: str = "moretti"
    POSTGRES_DB: str = "customer_db"

settings = Settings()  