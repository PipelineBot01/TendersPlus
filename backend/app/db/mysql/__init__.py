from sqlalchemy_utils.functions import database_exists, create_database

from config import settings

from .engine import engine, session, base
from .schema.university import SQLUniversity
from .schema.research_field import SQLResearchField
from .schema.user import SQLUser
from .schema.user_research_field import SQLUserResearchField
from .curd.university import sql_add_university


def init_db():
    # init database, check if database is existed or not
    if not database_exists(engine.url):
        create_database(engine.url)

    # init tables
    print(base.metadata.__dict__)
    base.metadata.drop_all(bind=engine)
    base.metadata.create_all(bind=engine)

    # init university table
    with session() as db:
        print(len(settings.UNIVERSITIES))
        for i in sorted(settings.UNIVERSITIES):
            print(i)
            sql_add_university(name=i,session=db)
        db.commit()
