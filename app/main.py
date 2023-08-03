from functools import lru_cache

from fastapi import FastAPI
from . import config


@lru_cache()
def get_settings():
    return config.Settings()


settings = get_settings()
app = FastAPI()


@app.get("/")
async def homepage():
    return {"hello": "world",
            "keyspace": settings.ASTRADB_KEYSPACE,
            'db_id': settings.ASTRADB_CLIENT_ID}
