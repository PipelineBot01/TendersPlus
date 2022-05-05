from sqlalchemy import Column, String, DATETIME, INT, ForeignKey
from ..engine import base


class SQLUserSubscribe(base):
    """
    status = 1, it means subscribed
    status = 0, it means unsubscribed

    last_date: last date sent a recommendation email
    """
    __tablename__ = 'user_subscribe'
    email = Column(String(128), ForeignKey('user.email'), primary_key=True)
    status = Column(INT, nullable=False, default=0)
    last_date = Column(DATETIME, nullable=True)
