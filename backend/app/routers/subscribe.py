"""
subscribe api allows user to subscribe the recommandation result or not
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.user import SubscribeModel
from dependencies import check_access_token, get_db
from db.mysql.curd.user_subscribe import sql_update_user_subscribe, sql_get_user_subscribe

router = APIRouter()


@router.post('')
async def subscribe(data: SubscribeModel, email: str = Depends(check_access_token), db: Session = Depends(get_db)):
    update = {'status': data.status}
    try:
        user_subscribe = sql_get_user_subscribe(email=email, session=db)
        sql_update_user_subscribe(user_subscribe, update, db)
        db.commit()
        return {'code': 200, 'data': ''}
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500, e)
