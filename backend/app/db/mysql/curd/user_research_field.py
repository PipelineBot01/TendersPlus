from sqlalchemy.orm import Session
from typing import List, Union

from ..schema.user_research_field import SQLUserResearchField


def sql_get_user_research_field(email: str, n: int, session: Session) -> Union[List[SQLUserResearchField], list]:
    return session.query(SQLUserResearchField.field_name, SQLUserResearchField.parent_field_name).filter(
        SQLUserResearchField.email == email).limit(n).all()
