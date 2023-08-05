import pathlib

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from . import db
from app.users.models import User
from .config import get_settings

from cassandra.cqlengine.management import sync_table

BASE_DIR = pathlib.Path(__file__).resolve().parent # app/
TEMPLATE_DIR = BASE_DIR / "templates"


settings = get_settings()
app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

@app.on_event("startup")
def on_startup():
    # treggered when fastapi starts
    print('BD works')
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        'request': request,
        'abc': 13324
    }
    return templates.TemplateResponse('home.html', context)


@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):

    return templates.TemplateResponse('auth/login.html', {'request': request})


@app.get('/users')
async def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)