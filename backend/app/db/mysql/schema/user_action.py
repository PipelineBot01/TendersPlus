from sqlalchemy import Column, String, DATETIME, ForeignKey, PrimaryKeyConstraint,TEXT
from ..engine import base


class SQLUserAction(base):
    """
    tpye:
    0: search,
    1: open link,
    2: save to favorite,
    3: remove from favorite.
    4: like the match result
    5: dislike the match result
    """
    __tablename__ = 'user_action'
    email = Column(String(128), ForeignKey('user.email'))
    type = Column(String(2), nullable=False)
    payload = Column(TEXT, nullable=False)
    action_date = Column(DATETIME,nullable=False)
    PrimaryKeyConstraint(email, action_date)
