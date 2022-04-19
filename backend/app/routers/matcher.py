
from fastapi import APIRouter, HTTPException,Depends

from dependencies import check_access_token
from models.matcher import MatcherModel
from utils.matcher.researcher import researcher_matcher
from db.mongo import curd
router = APIRouter()


@router.post('/researchers')
def match_researchers(data: MatcherModel):
    """
    Match similar researchers
    :param data:
    :return:
    """
    try:
        output = []
        if len(data.tags) != 0 or len(data.research_fields) != 0:
            output = researcher_matcher.match_by_profile(divs=data.research_fields, tags=data.tags)
        return {'code': 200, 'data': output}
    except Exception as e:
        print(e)
        raise HTTPException(500, str(e))

@router.post('/tenders')
async def match_tenders(data:MatcherModel,email:Depends(check_access_token)):
    """
    Match tenders via user's divisions, tags and email

    Parameters
    ----------
    data:
    email

    Returns
    -------

    """
    try:
        docs = await curd.db_get_latest_tenders(3)
        return {'code':200,'data':docs}
    except Exception as e:
        print(e)
        raise HTTPException(500, str(e))