from pydantic import BaseModel
from typing import List


class MatcherModel(BaseModel):
    research_fields:List[str]
    tags:List[str]
