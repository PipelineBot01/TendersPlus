from typing import List
from sqlalchemy.orm import Session
from datetime import datetime

from ..schema.user_action import SQLUserAction


def sql_add_user_action(email: str, type_: str, payload: str, session: Session):
    record = SQLUserAction(email=email, type=type_, payload=payload, action_date=datetime.now())
    session.add(record)


def sql_get_all_user_action(session: Session) -> List[SQLUserAction]:
    return session.query(SQLUserAction).all()

# def sql_get_user_action(email:str,type_:str,payload:str,session:Session):