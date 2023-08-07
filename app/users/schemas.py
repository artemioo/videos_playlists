from pydantic import BaseModel, EmailStr, SecretStr, validator, root_validator
from . import auth
from .models import User


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    token: str = None

    @root_validator
    def validate_user(cls, values):
        """ фунция которая валидирует юзера с помощью других методов и присваивает токен """
        err_msg = 'Incorrect email or password'
        email = values.get('email') or None
        password = values.get('password') or None
        if email is None or password is None:
            raise ValueError(err_msg)
        password = password.get_secret_value()  # SecretStr method, получаем пароль в открытом виде
        user_obj = auth.authenticate(email, password)

        token = auth.login(user_obj)
        return {'session_id': token}


class UserSignupSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr

    @validator('email')
    def email_available(cls, v, values, **kwargs):
        q = User.objects.filter(email=v)
        if q.count() != 0:
            raise ValueError('Email is not available')
        return v

    @validator("password_confirm")
    def password_match(cls, v, values, **kwargs):
        password = values.get('password')
        password_cofrim = v
        if password != password_cofrim:
            raise ValueError('Passwords do not match')
        return v



