from typing import Union, List

from sqlalchemy.orm import Session
from ..schema.user_favourite import SQLUserFavourite


def sql_add_user_favourite(email: str, id: str, session: Session) -> Union[SQLUserFavourite, None]:
    record = SQLUserFavourite(email=email, id=id)
    session.add(record)
    return record


def sql_get_user_favourite(email: str, session: Session) -> List[SQLUserFavourite]:
    # set limitation
    return session.query(SQLUserFavourite.id).filter_by(email=email).limit(50).all()


def sql_remove_user_favourite(email: str, id: str, session: Session) ->  Union[SQLUserFavourite, None]:
    record = session.query(SQLUserFavourite).filter_by(email=email, id=id).one_or_none()
    session.delete(record)
    return record
