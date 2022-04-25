import requests
import json
from fastapi import APIRouter, HTTPException, Depends

from dependencies import check_access_token
from models.matcher import MatcherModel
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
        response = requests.post('http://localhost:20222/get_sim_researchers',
                                 json={'divisions': data.research_fields,
                                       'tags': data.tags})
        if response.status_code == 200:
            output = json.loads(response.content)['data']
        return {'code': 200, 'data': output}
    except Exception as e:
        print(e)
        raise HTTPException(500, str(e))


@router.post('/tenders')
async def match_tenders(data: MatcherModel, email: str = Depends(check_access_token)):
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

        docs = []
        response = requests.post('http://localhost:20222/get_sim_researchers',
                                 json={'divisions': data.research_fields,
                                       'tags': data.tags})
        if response.status_code == 200:
            GO_ID = json.loads(response.content)['data']
            docs = curd.db_get_tenders_by_ids(GO_ID)

        return {'code': 200, 'data': docs}
    except Exception as e:
        print(e)
        raise HTTPException(500, str(e))
