from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import check_access_token, get_db, check_admin_token
from models.user import ActionModel
from db.mysql.curd.user_action import sql_add_user_action
from config import settings

router = APIRouter()


@router.post('')
async def add_user_action(data: ActionModel, email: str = Depends(check_access_token), db: Session = Depends(get_db)):
    try:
        sql_add_user_action(email=email, type_=data.type, payload=data.payload, session=db)
        db.commit()
        return {'code': 0, 'data': ''}
    except Exception as e:
        print(str(e))
        raise HTTPException(500)


# ====== admin api ======
@router.get('/all')
async def get_all_user_info(flag: bool = Depends(check_admin_token)):
    return {'code': 200, 'data': settings.USER_ACTION}
