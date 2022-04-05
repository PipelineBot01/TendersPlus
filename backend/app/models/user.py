from typing import List
from pydantic import BaseModel


class ProfileModel(BaseModel):
    first_name: str
    last_name: str
    university: str
    research_fields: List[str]
    tags: List[str]


class ActionModel(BaseModel):
    type: str
    payload: str
