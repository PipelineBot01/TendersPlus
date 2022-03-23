from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from dependencies import check_access_token, get_db
from db.mysql.curd.user import sql_get_user
from db.mysql.curd.user_research_field import sql_get_user_research_field
from db.mysql.curd.user_tag import sql_get_user_tag

router = APIRouter()


@router.get('')
def get_usr(email: str = Depends(check_access_token), db: Session = Depends(get_db)):
    try:
        user = sql_get_user(email, session=db)
        if user:
            data = user.__dict__
            user_research_field = sql_get_user_research_field(email=user.email, n=user.n_research_field, session=db)
            tmp_research_field = {}
            for i in user_research_field:
                if i.parent_field_name == 'none':
                    tmp_research_field[i.field_name] = []
                elif i.parent_field_name not in tmp_research_field:
                    tmp_research_field[i.parent_field_name] = [i.field_name]
                else:
                    tmp_research_field[i.parent_field_name].append(i.field_name)
            research_fields = []
            for k, v in tmp_research_field.items():
                tmp = {'field': k, 'sub_fields': v}
                research_fields.append(tmp)

            data['research_fields'] = research_fields

            user_tags = sql_get_user_tag(email=user.email, n=user.n_tag, session=db)
            data['tags'] = [i[0] for i in user_tags]
            return {'code': 0, 'data': data}
        raise HTTPException(404, 'USER NOT FOUND')
    except Exception as e:
        print(str(e))
        raise HTTPException(500, 'INTERNAL SERVER ERROR')
