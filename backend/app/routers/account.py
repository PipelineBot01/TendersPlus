from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.account import LoginModel, SignupModel
from dependencies import get_db
from db.mysql.curd.user import sql_get_user, sql_add_user
from db.mysql.curd.user_research_field import sql_get_user_research_field
from db.mysql.curd.user_tag import sql_get_user_tag
from db.mysql.curd.user_favourite import sql_get_user_favourite
from utils.auth import encode_password, generate_token
from config import settings

router = APIRouter()


@router.post('/login')
def login(data: LoginModel, db: Session = Depends(get_db)):
    user = sql_get_user(email=data.email, session=db)
    if user:
        if user.password == encode_password(data.password):
            access_token = generate_token(
                {'email': data.email, 'expire_date': (datetime.now() + timedelta(days=7)).timestamp()})

            tags = [i.name for i in sql_get_user_tag(email=user.email, n=user.n_tag, session=db)]
            research_fields = [{'field': i.field_id, 'sub_field': []} for i in
                               sql_get_user_research_field(email=user.email, n=user.n_research_field, session=db)]


            return {'code': 200, 'data': {'access_token': access_token,
                                          'first_name': user.first_name,
                                          'last_name': user.last_name,
                                          'university': user.university,
                                          'tags': tags,
                                          'research_fields': research_fields
                                    
                                          }}
        raise HTTPException(401, 'INVALID PASSWORD')
    raise HTTPException(404, 'USER NOT FOUND')


@router.post('/signup')
def signup(data: SignupModel, db: Session = Depends(get_db)):
    try:
        if data.password != data.confirmed_password:
            raise HTTPException(400, 'PASSWORDS MISMATCHING')
        if data.university not in settings.UNIVERSITIES:
            raise HTTPException(400, 'INVALID UNIVERSITY')
        for i in data.research_fields:
            if i not in settings.RESEARCH_FIELDS:
                raise HTTPException(400, f'INVALID RESEARCH FIELD {i}')
        user = sql_get_user(email=data.email, session=db)
        if user:
            raise HTTPException(403, 'EMAIL EXISTED')
        user = sql_add_user(email=data.email, password=data.password, first_name=data.first_name,
                            last_name=data.last_name,
                            n_research_field=len(data.research_fields),
                            university=data.university, research_field=data.research_fields, session=db)
        db.commit()
        access_token = generate_token(
            {'email': data.email, 'expire_date': (datetime.now() + timedelta(days=7)).timestamp()})
        return {'code': 200, 'data': {'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name,
                                      'university': user.university,
                                      'research_fields': [{'field': i, 'sub_field': []} for i in data.research_fields],
                                      'access_token': access_token}}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500, str(e))
