from enum import Enum
from functools import lru_cache

from pydantic import BaseSettings


class Engine(str, Enum):
    sqlite = "sqlite"
    postgresql = "postgresql"


class Settings(BaseSettings):
    API_DEBUG: bool = False
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    ROOT_TOKEN: str = "no_token"

    HTTPS_PROXY: str = ""

    DB_ENGINE: Engine = "sqlite"  # sqlite / postgresql

    POSTGRESQL_USERNAME: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int = 5432
    POSTGRESQL_DB_NAME: str

    SQLITE_DIR: str = "database/APIv2.db"


@lru_cache()
def settings():
    return Settings(
        _env_file=".env",
        _env_file_encoding="utf-8",
    )
