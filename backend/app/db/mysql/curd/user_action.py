from sqlalchemy.orm import Session
from datetime import datetime

from ..schema.user_action import SQLUserAction


def sql_add_user_action(email: str, type_: str, payload: str, session: Session):
    record = SQLUserAction(email=email, type=type_, payload=payload, action_date=datetime.now())
    session.add(record)
