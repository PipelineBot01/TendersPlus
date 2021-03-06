import base64
import json

import requests

from fastapi import APIRouter, HTTPException

from db.mongo import curd, mongo

router = APIRouter()


@router.get('')
async def get_opportunities(query: str = None, limit: int = 0, skip: int = 0):
    try:

        keywords = None
        if query:
            keywords = base64.b64decode(query).decode('utf-8')
        # print('keywords:', keywords)
        docs = await curd.db_get_tenders_by_keywords(keywords, limit, skip)
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
    return {'code': 200, 'data': count}


@router.get('/latest')
async def get_latest_opportunities(limit: int = 0, skip: int = 0):
    docs = await curd.db_get_latest_tenders(limit, skip)
    return {'code': 200, 'data': docs}


@router.get('/expiring')
async def get_expiring_opportunities(limit: int = 0, skip: int = 0):
    docs = await curd.db_get_expiring_tenders(limit, skip)
    return {'code': 200, 'data': docs}


@router.get('/hot')
async def get_hot_opportunities(limit: int = 0, skip: int = 0):
    docs = []
    try:
        response = requests.get('http://localhost:20222/get_hot_tenders', timeout=5)
    except:
        return {'code': 200, 'data': docs}

    if response.status_code == 200:
        content = json.loads(response.content)
        go_id = content['data']
        print('go_id', go_id)
        if limit != 0:
            go_id = go_id[:limit]
        docs = await curd.db_get_tenders_from_history_by_ids(go_id)
    # docs = await curd.db_get_expiring_tenders(n)
    return {'code': 200, 'data': docs}
