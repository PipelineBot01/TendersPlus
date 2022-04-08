from datetime import datetime
from sqlalchemy.orm import Session

from typing import Union, List

from utils import auth

from ..schema.user import SQLUser
from ..schema.user_research_field import SQLUserResearchField


def sql_get_user(email: str, session: Session) -> Union[SQLUser, None]:
    return session.query(SQLUser).filter(SQLUser.email == email).one_or_none()


def sql_add_user(email: str, password: str, first_name: str, last_name: str, university: str, n_research_field: int,
                 research_field: list, session: Session) -> SQLUser:
    encode_password = auth.encode_password(password)
    first_name_capital = first_name[0].upper() + first_name[1:]
    last_name_capital = last_name[0].upper() + last_name[1:]
    user_record = SQLUser(email=email, password=encode_password, first_name=first_name_capital,
                          last_name=last_name_capital,
                          n_research_field=n_research_field,
                          university=university, create_date=datetime.now(), status=1)
    session.add(user_record)
    for i in research_field:
        session.add(SQLUserResearchField(email=email, field_id=i))

    return user_record


def sql_get_all_users(session: Session) -> List[SQLUser]:
    return session.query(SQLUser).join(SQLUserResearchField, SQLUser.email == SQLUserResearchField.email).all()
