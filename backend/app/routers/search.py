import base64
from datetime import datetime

from fastapi import APIRouter, HTTPException

from db.mongo import crud
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
            print(doc)
            if 'close_date' in doc:
                doc['close_date'] = doc['close_date'].strftime(settings.DATETIME_FORMAT)
            else:
                doc['close_date'] = 'On going'

            if 'open_date' in doc:
                doc['open_date'] = doc['open_date'].strftime(settings.DATETIME_FORMAT)
            else:
                doc['open_date'] = ''

        return {'code': 200, 'data': docs}
    except Exception as e:
        print(str(e))
        raise HTTPException(500)
