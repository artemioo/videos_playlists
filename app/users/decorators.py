from fastapi import Request, HTTPException
from functools import wraps

from .auth import verify_user_id
from .exceptions import LoginRequiredException


def login_required(func):
    @wraps(func) #good pratice but don't required
    def wrapper(request: Request, *args, **kwargs):
        session_id = request.cookies.get('session_id', None)
        user_session = verify_user_id(session_id)
        if not user_session is None:
            raise LoginRequiredException(status_code=401)
        user_session = verify_user_id(session_id)
        return func(request, *args, **kwargs)
    return wrapper