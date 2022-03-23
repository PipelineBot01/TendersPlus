from sqlalchemy import Column, String, PrimaryKeyConstraint, INT, ForeignKey, BIGINT
from ..engine import base


class SQLUserResearchField(base):
    __tablename__ = 'user_research_field'
    email = Column(String(128), ForeignKey('user.email'), nullable=False)
    field_id = Column(String(128), ForeignKey('research_field.id'), nullable=False)
    PrimaryKeyConstraint(email, field_id)
