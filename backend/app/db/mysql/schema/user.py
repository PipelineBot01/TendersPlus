from sqlalchemy import Column, String, DATETIME, INT, ForeignKey, BIGINT
from ..engine import base


class SQLUser(base):
    __tablename__ = 'player'
    no = Column(autoincrement=True, primary_key=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    university = Column(String(128), ForeignKey('university.name'),nullable=True)
