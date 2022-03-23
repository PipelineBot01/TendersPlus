from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint

from ..engine import base


class SQLUserTag(base):
    __tablename__ = 'user_tag'
    name = Column(String(64), nullable=False)
    email = Column(String(128), ForeignKey('user.email'), nullable=False)
    PrimaryKeyConstraint(name, email)
