import pathlib
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from .users.decorators import login_required
from .users.schemas import (UserSignupSchema, UserLoginSchema)
from . import db, utils
from .users.models import User
from .config import get_settings
from app.shortcuts import render, redirect
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
        'abc': 13324
    }
    return render(request, 'home.html', context)


@app.get("/account", response_class=HTMLResponse)
@login_required
def account_view(request: Request):

    context = {}
    return render(request, 'account.html', context)


@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    session_id = request.cookies.get('session_id') or None
    return render(request, 'auth/login.html', {'logged_in': session_id is not None})


@app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request,
                    email: str = Form(...),
                    password: str = Form(...)):

    raw_data = {'email': email, 'password': password}
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
    context = {
                "data": data,
                "errors": errors,
            }
    if len(errors) > 0:
        return render(request, 'auth/login.html', context, status_code=400)

    return redirect("/", cookies=data)


@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render(request, 'auth/signup.html')


@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request,
                     email: str=Form(...),
                     password: str = Form(...),
                     password_confirm: str = Form(...)
                     ):
    raw_data  = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    if len(errors) > 0:
        return render(request, "auth/signup.html")
    return redirect('/login')


@app.get('/users')
async def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)