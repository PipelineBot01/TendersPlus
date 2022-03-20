from sqlalchemy import Column, String, INT
from ..engine import base


class SQLUser(base):
    __tablename__ = 'research_field'
    name = Column(String(128), primary_key=True)
    level = Column(INT, nullable=False)
    parent = Column(String(128), nullable=False)
