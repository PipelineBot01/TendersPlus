from sqlalchemy.orm import Session
from ..schema.user_tag import SQLUserTag


def sql_get_user_tag(email: str, n: int, session: Session) -> list:
    return session.query(SQLUserTag).filter(SQLUserTag.email == email).limit(n).all()


def sql_add_user_tag(email: str, name: str, session: Session) -> SQLUserTag:
    record = SQLUserTag(email=email, name=name)
    session.add(record)
    return record
