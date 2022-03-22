from sqlalchemy.orm import Session
from ..schema.university import SQLUniversity

def sql_add_university(name:str,session:Session)->None:
    if not session.query(SQLUniversity).filter(SQLUniversity.name==name).one_or_none():
        record = SQLUniversity(name=name)
        session.add(record)
