from .engine import engine, session
from sqlalchemy_utils.functions import database_exists, create_database


def init_db():
    # init database, check if database is existed or not
    if not database_exists(engine.url):
        create_database(engine.url)

    # init university table
