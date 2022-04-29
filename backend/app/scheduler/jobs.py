import numpy as np
import pandas as pd

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.interval import IntervalTrigger

from datetime import datetime
from config import settings
from db.mysql import session
from db.mysql.curd.user import sql_get_all_users
from db.mysql.curd.user_action import sql_get_all_user_action
from db.mysql.curd.user_research_field import sql_get_all_user_research_field
from db.mysql.curd.user_tag import sql_get_all_user_tag

jobs = []


def job(id: str, trigger: BaseTrigger, delay: bool = False):
    def decorator(fn):
        jobs.append({'id': id, 'trigger': trigger, 'func': fn, 'delay': delay})
        return fn

    return decorator


# @job(id='get_all_user_info', trigger=IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'), delay=False)
@job(id='get_all_user_info', trigger=IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'), delay=False)
async def get_all_user_info():
    # if len(settings.USER_INFO) == 0 or datetime.now().hour < 3:
    if True:
        with session() as db:
            df_all_user = pd.DataFrame.from_records(sql_get_all_users(db))
            if df_all_user.shape[0] !=0:
                df_all_user_research_field = pd.DataFrame.from_records(sql_get_all_user_research_field(db)).groupby('email',
                                                                                                                    as_index=False).agg(
                    {'field_id': lambda x: list(x)})
                df_all_user_research_field.rename(columns={'field_id': 'divisions'}, inplace=True)

                df_all_user_tag = pd.DataFrame.from_records(sql_get_all_user_tag(db)).groupby('email', as_index=False).agg(
                    {'name': lambda x: list(x)})
                df_all_user_tag.rename(columns={'name':'tags'},inplace=True)

                data = pd.merge(df_all_user_research_field, df_all_user_tag, how='left', on='email')
                data = pd.merge(df_all_user, data, how='inner', on='email')
                data.fillna('',inplace=True)

                settings.USER_INFO = data.to_dict('records')


@job(id='get_all_user_action', trigger=IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'), delay=False)
# @job(id='get_all_user_action', trigger=IntervalTrigger(minutes=5, timezone='Asia/Hong_Kong'), delay=False)
async def get_all_user_action():
    # if len(settings.USER_ACTION) == 0 or datetime.now().hour < 3:
    if True:
        with session() as db:
            settings.USER_ACTION = sql_get_all_user_action(db)
