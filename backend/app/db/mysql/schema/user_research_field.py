from sqlalchemy import Column, String, PrimaryKeyConstraint, INT, ForeignKey, BIGINT
from ..engine import base


class SQLUserResearchField(base):
    __tablename__ = 'user_research_field'
    email = Column(ForeignKey('user.email'), nullable=False)
    field_name = Column(String(128), ForeignKey('research_field.name'), nullable=False)
    parent_field_name = Column(String(128), ForeignKey('research_field.name'), nullable=False)
    level = Column(INT, nullable=False)
    PrimaryKeyConstraint(email, field_name)
