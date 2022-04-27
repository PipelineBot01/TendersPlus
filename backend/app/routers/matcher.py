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
        print('data:', data.__dict__)
        docs = []
        response = requests.post('http://localhost:20222/get_reco_tenders',
                                 json={'id': email, 'divisions': data.research_fields,
                                       'tags': data.tags})
        if response.status_code == 200:
            content = json.loads(response.content)
            GO_ID = content['data']
            print('go id:', GO_ID)
            docs = []
            for i in GO_ID:
                doc = await curd.db_get_tenders_from_history_by_id(i)
                if doc:
                    docs.append(doc)

        return {'code': 200, 'data': docs}
    except Exception as e:
        print(e)
        raise HTTPException(500, str(e))
