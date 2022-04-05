from sqlalchemy import Column, String, DATETIME, ForeignKey, PrimaryKeyConstraint
from ..engine import base


class SQLUserAction(base):
    """
    tpye, "0": search, "1": open link
    """
    __tablename__ = 'user_action'
    email = Column(String(128), ForeignKey('user.email'))
    type = Column(String(2), nullable=False)
    payload = Column(String(256), nullable=False)
    action_date = Column(DATETIME)
    PrimaryKeyConstraint(email, action_date)
