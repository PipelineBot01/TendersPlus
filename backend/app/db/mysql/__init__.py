from sqlalchemy_utils.functions import database_exists, create_database

from config import settings

from .engine import engine, session, base

from .schema.university import SQLUniversity
from .schema.research_field import SQLResearchField
from .schema.user import SQLUser
from .schema.user_tag import SQLUserTag
from .schema.user_research_field import SQLUserResearchField

from .curd.university import sql_add_university
from .curd.research_field import sql_add_research_field


def init_db():
    # init database, check if database is existed or not
    if not database_exists(engine.url):
        create_database(engine.url)

    # init tables

    # base.metadata.drop_all(bind=engine)
    base.metadata.create_all(bind=engine)

    with session() as db:

        # init university table
        for i in settings.UNIVERSITIES:
            sql_add_university(name=i, session=db)

        # init division
        for k, v in settings.RESEARCH_FIELDS.items():
            sql_add_research_field(id=k, name=v['field'], parent_name='none', level=1, session=db)
            for j in range(len(v['sub_fields'])):
                sql_add_research_field(id=f'{k}_{j}', name=v['sub_fields'][j], parent_name=v['field'], level=2,
                                       session=db)

        # special case
        sql_add_research_field(id='d_00', name='none', parent_name='none', level=0, session=db)
        db.commit()
