from sqlalchemy import Column, String, DATETIME, INT, ForeignKey
from ..engine import base


class SQLUser(base):
    """
    status=1: inactive, status =0 active
    """
    __tablename__ = 'user'
    email = Column(String(128), primary_key=True)
    password = Column(String(200), nullable=False)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    university = Column(String(128), nullable=False)
    create_date = Column(DATETIME, nullable=False)
    status = Column(INT, nullable=False)
    n_research_field = Column(INT, nullable=False, default=0)
    n_tag = Column(INT, nullable=False, default=0)
