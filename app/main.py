from fastapi import FastAPI
from . import db
from app.users.models import User
from .config import get_settings

from cassandra.cqlengine.management import sync_table



settings = get_settings()
app = FastAPI()


@app.on_event("startup")
def on_startup():
    # treggered when fastapi starts
    print('BD works')
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get("/")
async def homepage():
    return {"hello": "world",
            "keyspace": settings.ASTRADB_KEYSPACE,
            'db_id': settings.ASTRADB_CLIENT_ID}


@app.get('/users')
async def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)