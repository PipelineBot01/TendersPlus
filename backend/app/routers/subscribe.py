"""
subscribe api allows user to subscribe the recommandation result or not
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from sqlalchemy.orm import Session

from models.user import SubscribeModel
from dependencies import check_access_token, get_db
from db.mysql.curd.user_subscribe import sql_update_user_subscribe, sql_get_user_subscribe, sql_add_user_subscribe
from utils.auto_email import create_sender, create_html_message

router = APIRouter()


@router.post('')
async def subscribe(data: SubscribeModel, email: str = Depends(check_access_token), db: Session = Depends(get_db)):
    update = {'status': data.status}
    try:
        user_subscribe = sql_get_user_subscribe(email=email, session=db)
        if user_subscribe is None:
            user_subscribe = sql_add_user_subscribe(email=email, session=db)

        sql_update_user_subscribe(user_subscribe, update)
        db.commit()
        return {'code': 200, 'data': ''}
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500, str(e))


@router.post('/send')
async def send_email(background_task: BackgroundTasks):
    fm = create_sender()

    message = create_html_message([], ['gongsakura@yahoo.com'
                                       ])

    background_task.add_task(fm.send_message, message)
