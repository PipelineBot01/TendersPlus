from sqlalchemy import Column, String, INT
from ..engine import base


class SQLResearchField(base):
    __tablename__ = 'research_field'
    id = Column(String(8), primary_key=True)
    name = Column(String(128), unique=True)
    parent_name = Column(String(128), nullable=False)
    level = Column(INT, nullable=False)
