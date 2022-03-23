from pydantic import BaseModel, EmailStr, validator
from typing import List


class LoginModel(BaseModel):
    email: EmailStr
    password: str

    @validator('email')
    def validate_email(cls, value):
        if not value:
            raise ValueError('EMPTY EMAIL')

    @validator('password')
    def validate_email(cls, value):
        if not value:
            raise ValueError('EMPTY PASSWORD')


class SignupModel(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    university: str
    password: str
    confirmed_password: str
    research_fields: List[str]

    @validator('email')
    def validate_email(cls, value):
        if not value:
            raise ValueError('EMPTY EMAIL')
        return value

    @validator('password')
    def validate_password(cls, value):
        if not value:
            raise ValueError('EMPTY PASSWORD')
        return value

    @validator('first_name')
    def validate_first_name(cls, value):
        if not value:
            raise ValueError('EMPTY FIRST NAME')
        return value

    @validator('last_name')
    def validate_last_name(cls, value):
        if not value:
            raise ValueError('EMPTY LAST NAME')
        return value

