import pandas as pd
import requests
import json
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.interval import IntervalTrigger

from datetime import datetime
from config import settings
from db.mysql import session
from db.mysql.curd.user import sql_get_all_users, sql_get_user
from db.mysql.curd.user_action import sql_get_all_user_action
from db.mysql.curd.user_research_field import sql_get_all_user_research_field
from db.mysql.curd.user_tag import sql_get_all_user_tag
from db.mongo.curd import db_get_tenders_from_history_by_id
from utils.auto_email import create_sender, create_html_message

jobs = []


def job(id: str, trigger: BaseTrigger, delay: bool = False):
    def decorator(fn):
        jobs.append({'id': id, 'trigger': trigger, 'func': fn, 'delay': delay})
        return fn

    return decorator


@job(id='get_all_user_info', trigger=IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'), delay=False)
async def get_all_user_info():
    with session() as db:
        record_1 = sql_get_all_users(db)
        if record_1:
            record_2 = sql_get_all_user_research_field(db)
            if record_2:
                record_3 = sql_get_all_user_tag(db)
                if record_3:
                    df_all_user = pd.DataFrame.from_records(record_1)
                    df_all_user_research_field = pd.DataFrame.from_records(record_2).groupby('email',
                                                                                             as_index=False).agg(
                        {'field_id': lambda x: list(x)})

                    df_all_user_research_field.rename(columns={'field_id': 'divisions'}, inplace=True)
                    df_all_user_tag = pd.DataFrame.from_records(record_3).groupby('email', as_index=False).agg(
                        {'name': lambda x: list(x)})

                    df_all_user_tag.rename(columns={'name': 'tags'}, inplace=True)
                    data = pd.merge(df_all_user_research_field, df_all_user_tag, how='left', on='email')
                    data = pd.merge(df_all_user, data, how='inner', on='email')
                    data.fillna('', inplace=True)
                    settings.USER_INFO = data.to_dict('records')
                    settings.USER_INFO_DF = data.set_index('email').to_dict('index')
                    print('settings.USER_INFO_DF', settings.USER_INFO_DF)


@job(id='get_all_user_action', trigger=IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'), delay=False)
async def get_all_user_action():
    with session() as db:
        settings.USER_ACTION = sql_get_all_user_action(db)


@job(id='send_recommendation', trigger=IntervalTrigger(minutes=5, timezone='Asia/Hong_Kong'), delay=False)
async def send_recommendation():
    data = settings.USER_INFO_DF
    print('send_recommendation start')
    if data:
        user = data['ryan@anu.com']

        response = requests.post('http://localhost:20222/get_reco_tenders',
                                 json={'id': 'ryan@anu.com', 'divisions': user['divisions'],
                                       'tags': (user['tags'] or [])})

        if response.status_code == 200:
            content = json.loads(response.content)
            GO_ID = content['data']
            docs = []
            for i in GO_ID:
                doc = await db_get_tenders_from_history_by_id(i)
                if doc:
                    docs.append(doc)
            sender = create_sender()
            message = create_html_message(docs[:3], ['gongsakura@yahoo.com', 'u7078049@anu.edu.au'])
            await sender.send_message(message)
    else:
        print('skip send_recommendation')
