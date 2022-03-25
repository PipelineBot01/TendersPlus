from pydantic import BaseModel
from typing import List


class ResearcherMatcherModel(BaseModel):
    research_fields:List[str]
    tags:List[str]