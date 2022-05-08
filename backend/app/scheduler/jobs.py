import pandas as pd
import requests
import json
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.interval import IntervalTrigger

from datetime import datetime, timedelta
from config import settings
from db.mysql import session
from db.mysql.curd.user import sql_get_all_users, sql_get_user
from db.mysql.curd.user_action import sql_get_all_user_action
from db.mysql.curd.user_research_field import sql_get_all_user_research_field
from db.mysql.curd.user_tag import sql_get_all_user_tag
from db.mysql.curd.user_subscribe import sql_get_all_users_needed_send_email
from db.mongo.curd import db_get_tenders_from_history_by_ids
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


@job(id='get_all_user_action', trigger=IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'), delay=False)
async def get_all_user_action():
    with session() as db:
        settings.USER_ACTION = sql_get_all_user_action(db)


@job(id='send_recommendation', trigger=IntervalTrigger(minutes=1, timezone='Asia/Hong_Kong'), delay=True)
async def send_recommendation():
    if 0 < datetime.now().hour < 24:
        print('start send_recommendation ')
        try:
            with session() as db:
                recipients = sql_get_all_users_needed_send_email(db, datetime.now() - timedelta(days=1))
                print('recipients:',recipients)
                sender = create_sender()
                for r in recipients:
                    user_df = settings.USER_INFO_DF[settings.USER_INFO_DF['email'] == r.email]
                    if user_df:
                        try:
                            response = requests.post('http://localhost:20222/get_reco_tenders',
                                                     json={'id': r.email, 'divisions': user_df['divisions'],
                                                           'tags': (user_df['tags'] or [])})
                            if response.status_code == 200:
                                go_id = json.loads(response.content)['data'][:3]
                                docs = db_get_tenders_from_history_by_ids(go_id)
                                if docs:
                                    await sender.send_message(create_html_message(docs, [r.email]))
                                    r.last_date = datetime.now()
                                    db.commit()
                            else:
                                print(f'Send recommendation error: user:{r.email}, exception:{response.content}')
                        except Exception as e:
                            print(f'Send recommendation error: user:{r.email}, exception:{str(e)}')
        except Exception as e:
            print(f'Send recommendation error: exception:{str(e)}')

        # ========================== original version =================================
        # response = requests.post('http://localhost:20222/get_reco_recipient')
        # if response.status_code == 200:
        #     content = json.loads(response.content)
        #     data = content['data']
        #     sender = create_sender()
        #     with session() as db:
        #         for k, v in data.items:
        #             print('recipient:', k, 'go_id:', v)
        #             recipient = sql_get_user_subscribe(email=k, session=db)
        #             if recipient and recipient.status == 1:
        #                 go_id = v
        #                 if go_id:
        #                     docs = await db_get_tenders_from_history_by_ids(go_id)
        #                     if docs:
        #                         await sender.send_message(create_html_message(docs, [recipient]))
        # else:
        #     print(f'{datetime.now()}    request error: {response.status_code} {response.content}')
