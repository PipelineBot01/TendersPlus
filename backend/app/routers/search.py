import base64
import datetime

from fastapi import APIRouter, HTTPException

from db.mongo import crud, mongo
from config import settings

router = APIRouter()


@router.get('')
async def get_open_opportunities(query: str = None):
    try:

        keywords = None
        if query:
            keywords = base64.b64decode(query).decode('utf-8')
        print('keywords:', keywords)
        docs = await crud.db_get_opportunities(keywords)
        for doc in docs:
            if isinstance(doc['close_date'], datetime.date):
                doc['close_date'] = doc['close_date'].strftime(settings.DATETIME_FORMAT)

            if isinstance(doc['open_date'], datetime.date):
                doc['open_date'] = doc['open_date'].strftime(settings.DATETIME_FORMAT)

        return {'code': 200, 'data': docs}
    except Exception as e:
        print(str(e))
        raise HTTPException(500)


@router.get('/total')
async def get_open_opportunities_count():
    return {'code': 200, 'data': mongo['tenders_client_docs_count']['clean_grants_opened']}


@router.get('/latest')
async def get_latest_opportunities(n: int = 3):

    docs = await crud.db_get_latest_tenders(n)
    for doc in docs:
        if isinstance(doc['close_date'], datetime.date):
            doc['close_date'] = doc['close_date'].strftime(settings.DATETIME_FORMAT)

        if isinstance(doc['open_date'], datetime.date):
            doc['open_date'] = doc['open_date'].strftime(settings.DATETIME_FORMAT)
    print(docs)
    return {'code': 200, 'data': docs}


@router.get('/expiring')
async def get_expiring_opportunities(n: int = 3):
    docs = await crud.db_get_expiring_tenders(n)
    for doc in docs:
        if isinstance(doc['close_date'], datetime.date):
            doc['close_date'] = doc['close_date'].strftime(settings.DATETIME_FORMAT)

        if isinstance(doc['open_date'], datetime.date):
            doc['open_date'] = doc['open_date'].strftime(settings.DATETIME_FORMAT)

    return {'code': 200, 'data': docs}
