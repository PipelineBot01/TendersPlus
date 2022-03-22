from sqlalchemy.orm import Session
from ..schema.research_field import SQLResearchField


def sql_add_research_field(name: str, parent_name: str, level: int, session: Session):
    if not session.query(SQLResearchField).filter(SQLResearchField.name == name).one_or_none():
        record = SQLResearchField(name=name, parent_name=parent_name, level=level)
        session.add(record)
