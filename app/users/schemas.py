from pydantic import BaseModel, EmailStr, SecretStr, validator

from .models import User


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


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr