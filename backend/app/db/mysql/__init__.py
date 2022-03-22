from .engine import engine, session,base
from sqlalchemy_utils.functions import database_exists, create_database


def init_db():
    # init database, check if database is existed or not
    if not database_exists(engine.url):
        create_database(engine.url)

    # init tables
    base.metadata.create_all(bind=engine)

    # init university table
