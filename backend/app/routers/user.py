from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from dependencies import check_access_token, get_db, check_admin_token
from db.mysql.curd.user import sql_get_user
from db.mysql.curd.user_research_field import sql_get_user_research_field, sql_add_user_research_field
from db.mysql.curd.user_tag import sql_get_user_tag, sql_add_user_tag
from db.mysql.curd.user_favourite import sql_get_user_favourite

from models.user import ProfileModel
from config import settings

router = APIRouter()


@router.get('')
def get_user(email: str = Depends(check_access_token), db: Session = Depends(get_db)):
    try:
        user = sql_get_user(email, session=db)
        if user:
            data = user.__dict__
            user_research_field = sql_get_user_research_field(email=user.email, n=user.n_research_field, session=db)
            research_fields = []

            for i in user_research_field:
                tmp = {'field': i.field_id, 'sub_fields': []}
                research_fields.append(tmp)

            data['research_fields'] = research_fields

            user_tags = sql_get_user_tag(email=user.email, n=user.n_tag, session=db)
            data['tags'] = [i.name for i in user_tags]

            user_favourite_tenders = sql_get_user_favourite(email=user.email, session=db)
            data['favourite_tenders'] = [i.id for i in user_favourite_tenders]
            return {'code': 0, 'data': data}
        raise HTTPException(404, 'USER NOT FOUND')
    except Exception as e:
        print(str(e))
        raise HTTPException(500, 'INTERNAL SERVER ERROR')


@router.post('')
def set_user(payload: ProfileModel, email: str = Depends(check_access_token), db: Session = Depends(get_db)):
    try:
        user = sql_get_user(email, db)
        if user:
            # update research fields
            research_fields = sql_get_user_research_field(email=email, n=user.n_research_field, session=db)
            user.n_research_field = len(payload.research_fields)

            for i in research_fields:
                if i.field_id not in payload.research_fields:
                    db.delete(i)
                else:
                    payload.research_fields.remove(i.field_id)
            for i in payload.research_fields:
                sql_add_user_research_field(email=email, field_id=i, session=db)

            # update tags
            tags = sql_get_user_tag(email=email, n=user.n_tag, session=db)
            user.n_tag = len(payload.tags)
            for i in tags:
                if i.name not in payload.tags:
                    db.delete(i)
                else:
                    payload.tags.remove(i.name)
            for i in payload.tags:
                sql_add_user_tag(email=email, name=i, session=db)

            # update basic info
            user.first_name = payload.first_name
            user.last_name = payload.last_name
            user.university = payload.university
            db.commit()
            return {'code': 200, 'data': ''}

        raise HTTPException(404, 'USER NOT FOUND')
    except Exception as e:
        print(str(e))
        raise HTTPException(500, 'INTERNAL SERVER ERROR')


# ====== admin api ======
@router.get('/all')
async def get_all_user_info(flag: bool = Depends(check_admin_token)):
    return {'code': 200, 'data': settings.USER_INFO}
