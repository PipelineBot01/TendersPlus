"""
The models package is used to define the api body data format
"""

from pydantic import BaseModel, EmailStr
from typing import List


class SubscribeModel(BaseModel):
    email: EmailStr
    tags: List[str]
