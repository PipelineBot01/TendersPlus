from sqlalchemy.orm import Session

from db.mysql.engine import session


def get_db() -> Session:
    db = session()
    try:
        yield db
    finally:
        db.close()
