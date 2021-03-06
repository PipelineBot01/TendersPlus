from sqlalchemy import Column, String, DATETIME, ForeignKey, PrimaryKeyConstraint
from ..engine import base


class SQLUserFavourite(base):
    """
    tpye, "0": search,
          "1": open link
          "2": add to favourite,
          "3" remove from favourite
    """
    __tablename__ = 'user_favourite'
    email = Column(String(128), ForeignKey('user.email'))
    id = Column(String(128), nullable=False)
    PrimaryKeyConstraint(email, id)
