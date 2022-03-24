from pydantic import BaseModel


class ResearcherMatcherModel():
    research_fields:list[str]
    tags:list[str]