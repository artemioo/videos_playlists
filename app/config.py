from pydantic import BaseSettings, Field
from typing import Optional
from dotenv import dotenv_values
from functools import lru_cache
# env_values = dotenv_values(".env")
# print(env_values)
import os

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'

class Settings(BaseSettings):
    ASTRADB_KEYSPACE: str
    ASTRADB_CLIENT_ID: str
    ASTRADB_CLIENT_SECRET: str
    # model_config = SettingsConfigDict(env_file='//.env')  pydantic v2

    class Config:
        env_file = '.env'


@lru_cache # кэширем чтоб не создавать объект много раз
def get_settings():
    return Settings()
