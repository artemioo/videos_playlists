import pathlib
import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from pydantic.error_wrappers import ValidationError
from .users.schemas import UserSignupSchema, UserLoginSchema
from . import db, utils
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


@app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request,
                    email: str = Form(...),
                    password: str = Form(...)):

    raw_data = {'email': email, 'password': password}
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)

    return templates.TemplateResponse('auth/signup.html',
                                      {'request': request,
                                       'data': data,
                                       'errors': errors})



@app.get("/signup", response_class=HTMLResponse)
def login_get_view(request: Request):
    return templates.TemplateResponse('auth/signup.html', {'request': request})


@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request,
                    email: str = Form(...),
                    password: str = Form(...),
                    password_confirm: str = Form(...)):

    raw_data = {'email': email, 'password': password, 'password_confirm': password_confirm}
    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)

    return templates.TemplateResponse('auth/signup.html',
                                      {'request': request,
                                       'data': data,
                                       'errors': errors})


@app.get('/users')
async def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)