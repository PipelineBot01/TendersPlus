from typing import List
from pydantic import BaseModel, validator


class ProfileModel(BaseModel):
    first_name: str
    last_name: str
    university: str
    research_fields: List[str]
    tags: List[str]

    @validator('research_fields')
    def validate_research_fields(cls, value):
        if len(value) > 3:
            raise ValueError('RESEARCH FIELDS NUMBER EXCEED 3')
        return value

    @validator('tags')
    def validate_tags(cls, value):
        if len(value) > 10:
            raise ValueError('TAGS NUMBER EXCEED 10')
        return value


class ActionModel(BaseModel):
    type: str
    payload: str


class SubscribeModel(BaseModel):
    status: int

    @validator('status')
    def validate_status(cls, value):
        if value != 0 and value != 1:
            raise ValueError('INVALID STATUS')
        return value
