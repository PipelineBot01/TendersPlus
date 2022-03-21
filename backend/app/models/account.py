from pydantic import BaseModel, EmailStr
from typing import List


class LoginModel(BaseModel):
    email: EmailStr
    password: str


class SignupModel(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    university: str
    password: str
    confirmed_password: str
    research_field: List[str]
