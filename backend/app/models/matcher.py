from pydantic import BaseModel


class ResearcherMatcherModel(BaseModel):
    research_fields:list[str]
    tags:list[str]