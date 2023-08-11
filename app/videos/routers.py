from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from app.users.decorators import login_required
from app.shortcuts import render, redirect
from app.utils import valid_schema_data_or_error
from .schemas import VideoCreateSchema
router = APIRouter(
    prefix='/videos',
    tags=['videos']
)


@router.get('/', response_class=HTMLResponse)
def video_list_view(request: Request):
    return render(request, "videos/list.html", {})


@router.get('/create', response_class=HTMLResponse)
@login_required
def video_create_view(request: Request):
    return render(request, "videos/create.html", {})


@router.post('/create', response_class=HTMLResponse)
@login_required
def video_create_post_view(request: Request, url: str = Form(...)):
    raw_data = {
        "url": url,
        "user_id": request.user.username,
    }
    data, errors = valid_schema_data_or_error(raw_data, VideoCreateSchema)
    context = {
        'data': data,
        "errors": errors,
        "url": url,
    }
    if len(errors) > 0:
        return render(request, 'videos/create.html', context, status_code=400)
    redirect_path = data.get('path') or '/videos/create'
    return redirect(redirect_path)


@router.get('/detail', response_class=HTMLResponse)
def video_detail_view(request: Request):
    return render(request, "videos/detail.html", {})