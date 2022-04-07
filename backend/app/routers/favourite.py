from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db.mysql.curd.user_favourite import sql_get_user_favourite, sql_add_user_favourite, sql_remove_user_favourite
from db.mongo.curd import db_get_tenders_by_id

from models.favourite import FavouriteTenderModel
from dependencies import get_db, check_access_token

router = APIRouter()


@router.get('')
async def get_user_favourite_tenders(email: str = Depends(check_access_token), db: Session = Depends(get_db)):
    try:
        user_favourite_tenders_id = sql_get_user_favourite(email=email, session=db)

        docs = [await db_get_tenders_by_id(i) for i in user_favourite_tenders_id]
        return {'code': 200, 'data': docs}
    except Exception as e:
        print(str(e))
        raise HTTPException(500, str(e))

@router.get('/id')
async def get_user_favourite_tenders_id(email: str = Depends(check_access_token), db: Session = Depends(get_db)):
    try:
        user_favourite_tenders_id = sql_get_user_favourite(email=email, session=db)
        return {'code': 200, 'data': [i.id for i in user_favourite_tenders_id]}
    except Exception as e:
        print(str(e))
        raise HTTPException(500, str(e))

@router.post('/add')
async def add_user_favourite_tender(data: FavouriteTenderModel, email: str = Depends(check_access_token),
                                    db: Session = Depends(get_db)):
    try:
        sql_add_user_favourite(email=email, id=data.id, session=db)
        db.commit()
        return {'code': 200, 'data': ''}
    except Exception as e:
        print(str(e))
        raise HTTPException(500, str(e))


@router.post('/remove')
async def remove_user_favourite_tender(data: FavouriteTenderModel, email: str = Depends(check_access_token),
                                    db: Session = Depends(get_db)):
    try:
        sql_remove_user_favourite(email=email, id=data.id, session=db)
        db.commit()
        return {'code': 200, 'data': ''}
    except Exception as e:
        print(str(e))
        raise HTTPException(500, str(e))
