import json
from fastapi import APIRouter, HTTPException

from models.matcher import ResearcherMatcherModel
from utils.matcher.researcher import researcher_matcher


router = APIRouter()


@router.post('/researchers')
def match_researchers(data: ResearcherMatcherModel):
    # try:
    output = []
    print(data.tags, data.research_fields)
    if len(data.tags) != 0 or len(data.research_fields) != 0:

        output = researcher_matcher.match_by_profile(divs=data.research_fields, tags=data.tags)
        print(output)
    return {'code': 200, 'data':  output}
    # except Exception as e:
    #     print(e)
    #     raise HTTPException(500, str(e))