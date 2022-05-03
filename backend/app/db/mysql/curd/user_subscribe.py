from typing import Union
from sqlalchemy.orm import Session

from ..schema.user_subscribe import SQLUserSubscribe



def sql_get_user_subscribe(email: str, session: Session) -> Union[None, SQLUserSubscribe]:
    return session.query(SQLUserSubscribe).filter(SQLUserSubscribe.email == email).one_or_none()


def sql_add_user_subscribe(email: str, session: Session) -> SQLUserSubscribe:
    record = SQLUserSubscribe(email=email)
    session.add(record)
    return record


def sql_update_user_subscribe(user_subscribe: SQLUserSubscribe, update: dict) -> None:
    """
       it has to be flushed
       """
    for k, v in update.items():
        setattr(user_subscribe, k, v)
