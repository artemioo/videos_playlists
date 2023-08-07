import datetime
import secrets
from jose import jwt, ExpiredSignatureError
from .models import User
from app import config


settings = config.get_settings()


def authenticate(email, password): # check and verify (step 1)
    try:
        user_obj = User.objects.get(email=email)
    except Exception:
        raise ValueError('User does not exist')
    if user_obj.verify_password(password) is None:
        return None
    return user_obj


def login(user_obj, expires=5):  # set cookie(token) (step 2)
    raw_data = {
        "user_id": f'{user_obj.user_id}',
        "role": "admin",
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires)
    }
    return jwt.encode(raw_data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_user_id(token):  # (step 3)
    data = None
    try:
        data = jwt.decode(token,  settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except ExpiredSignatureError as e:
        print(e)
    except:
        pass
    if 'user_id' not in data:
        return None
    return data
