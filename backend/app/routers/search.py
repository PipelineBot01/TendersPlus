import base64
import json

import requests

from fastapi import APIRouter, HTTPException

from db.mongo import curd, mongo

router = APIRouter()


@router.get('')
async def get_open_opportunities(query: str = None):
    try:

        keywords = None
        if query:
            keywords = base64.b64decode(query).decode('utf-8')
        # print('keywords:', keywords)
        docs = await curd.db_get_tenders_by_keywords(keywords)
        # print(docs)
        return {'code': 200, 'data': docs}
    except Exception as e:
        print(str(e))
        raise HTTPException(500)


@router.get('/count')
async def get_open_opportunities_count():
    count = 0
    if 'clean_grants_all' in mongo['tenders_client_docs_count']:
        count = mongo['tenders_client_docs_count']['clean_grants_all']
    return {'code': 200, 'data': count }


@router.get('/latest')
async def get_latest_opportunities(n: int = 0):
    docs = await curd.db_get_latest_tenders(n)
    return {'code': 200, 'data': docs}


@router.get('/expiring')
async def get_expiring_opportunities(n: int = 0):
    docs = await curd.db_get_expiring_tenders(n)
    return {'code': 200, 'data': docs}


@router.get('/hot')
async def get_hot_opportunities(n: int = 0):
    response = requests.get('http://localhost:20222/get_hot_tenders')
    docs = []
    if response.status_code == 200:
        content = json.loads(response.content)
        go_id = content['data']
        print(go_id)
        if n != 0:
            go_id = go_id[:n]
        docs = await curd.db_get_tenders_from_history_by_ids(go_id)
    # docs = await curd.db_get_expiring_tenders(n)
    return {'code': 200, 'data': docs}
