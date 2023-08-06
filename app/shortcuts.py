from app.config import get_settings
from starlette.templating import Jinja2Templates


settings = get_settings()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


def render(request, template_name, context):
    ctx = context.copy()
    ctx.update({'request': request})
    return templates.TemplateResponse(template_name, ctx)