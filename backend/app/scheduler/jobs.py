from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.interval import IntervalTrigger

from datetime import datetime
from config import settings
from db.mysql import session
from db.mysql.curd.user import sql_get_all_users
from db.mysql.curd.user_action import sql_get_all_user_action

jobs = []


def job(id: str, trigger: BaseTrigger, delay: bool = False):
    def decorator(fn):
        jobs.append({'id': id, 'trigger': trigger, 'func': fn, 'delay': delay})
        return fn

    return decorator


@job(id='get_all_user_info', trigger=IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'), delay=False)
async def get_all_user_info():
    if len(settings.USER_INFO) == 0 or datetime.now().hour < 3:
        with session() as db:
            settings.USER_INFO = sql_get_all_users(db)


@job(id='get_all_user_action', trigger=IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'), delay=False)
async def get_all_user_action():
    if len(settings.USER_ACTION) == 0 or datetime.now().hour < 3:
        with session() as db:
            settings.USER_ACTION = sql_get_all_user_action(db)
