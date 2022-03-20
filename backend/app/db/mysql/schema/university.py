from sqlalchemy import Column, String
from ..engine import base


class SQLUser(base):
    __tablename__ = 'university'
    name = Column(String(128), primary_key=True)
