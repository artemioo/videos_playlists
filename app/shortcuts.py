from starlette.responses import HTMLResponse, RedirectResponse

from app.config import get_settings
from starlette.templating import Jinja2Templates


settings = get_settings()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


def redirect(path, cookies: dict = {}):
    response = RedirectResponse(path, status_code=302)
    for k, v in cookies.items():
        response.set_cookie(key=k, value=v, httponly=True)
    return response


def render(request, template_name, context={}, status_code: int=200, cookies: dict = {}):
    """ возвращает response класса HTMLResponse в котором лежит название шаблона+request+status code+cookie"""
    ctx = context.copy()
    ctx.update({'request': request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)  # class Template method render, This will return the rendered template as a string.
    response = HTMLResponse(html_str, status_code=status_code)
    # response.set_cookie(key='dark mode', value=1)
    if len(cookies.keys()) > 0:
        # set httponly cookies
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)
    # delete cookies
    # for key in request.cookies.keys():
    #      response.delete_cookie(key)
    return response
