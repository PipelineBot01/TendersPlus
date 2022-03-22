from sqlalchemy import Column, String, INT
from ..engine import base


class SQLResearchField(base):
    __tablename__ = 'research_field'
    name = Column(String(128), primary_key=True,unique=True)
    parent_name = Column(String(128), nullable=False,unique=True)
    level = Column(INT, nullable=False)

