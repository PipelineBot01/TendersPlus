from typing import Union, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime

from ..schema.user_subscribe import SQLUserSubscribe


def sql_get_user_subscribe(email: str, session: Session) -> Union[None, SQLUserSubscribe]:
    return session.query(SQLUserSubscribe).filter(SQLUserSubscribe.email == email).one_or_none()


def sql_add_user_subscribe(email: str, session: Session) -> SQLUserSubscribe:
    record = SQLUserSubscribe(email=email)
    session.add(record)
    return record


def sql_get_all_subscribed_users(session: Session) -> List[SQLUserSubscribe]:
    return session.query(SQLUserSubscribe).filter(SQLUserSubscribe.status == 1).all()


def sql_get_all_users_needed_send_email(session: Session, date: datetime) -> List[SQLUserSubscribe]:
    return session.query(SQLUserSubscribe).filter(
        and_(SQLUserSubscribe.status == 1, SQLUserSubscribe.last_date <= date)).limit(5).all()


def sql_update_user_subscribe(user_subscribe: SQLUserSubscribe, update: dict) -> None:
    """
       it has to be flushed
       """
    for k, v in update.items():
        setattr(user_subscribe, k, v)
