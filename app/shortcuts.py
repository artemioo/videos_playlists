from starlette.responses import HTMLResponse

from app.config import get_settings
from starlette.templating import Jinja2Templates


settings = get_settings()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


def render(request, template_name, context={}, status_code: int=200):
    ctx = context.copy()
    ctx.update({'request': request})

    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse('something', status_code=status_code)
    return response
    # return templates.TemplateResponse(template_name, ctx)