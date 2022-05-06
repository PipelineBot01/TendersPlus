from sqlalchemy.orm import Session
from typing import List, Union

from ..schema.user_research_field import SQLUserResearchField


def sql_get_user_research_field(email: str, n: int, session: Session) -> Union[List[SQLUserResearchField], list]:
    return session.query(SQLUserResearchField).filter(
        SQLUserResearchField.email == email).limit(n).all()


def sql_add_user_research_field(email: str, field_id: str, session: Session) -> SQLUserResearchField:
    record = SQLUserResearchField(email=email, field_id=field_id)
    session.add(record)
    return record


def sql_get_all_user_research_field(session: Session):
    return [i.__dict__ for i in session.query(SQLUserResearchField).all()]
