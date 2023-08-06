from pydantic import BaseSettings, Field
from typing import Optional
from dotenv import dotenv_values
from functools import lru_cache
from pathlib import Path
import os

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent
    TEMPLATES_DIR: Path = Path(__file__).resolve().parent / 'templates'
    ASTRADB_KEYSPACE: str
    ASTRADB_CLIENT_ID: str
    ASTRADB_CLIENT_SECRET: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = Field(default='HS256')
    # model_config = SettingsConfigDict(env_file='//.env')  pydantic v2

    class Config:
        env_file = '.env'


@lru_cache # кэширем чтоб не создавать объект много раз
def get_settings():
    return Settings()
