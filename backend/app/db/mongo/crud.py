from datetime import datetime, timedelta

from sympy import re
from config import settings
from typing import Union
import pandas as pd

from motor.motor_asyncio import AsyncIOMotorCollection
from engine import mongo


async def db_get_latest_tenders(n: Union[int, None] = None) -> dict:
    """
    if n =None, get all related tenders
    """
    collection = mongo['tenders_client']['tenders']['open']
    condition = {}
    limit = n
    docs = await do_find(collection=collection, condition=condition, limit=limit)

    latest_datetime = datetime.now() - timedelta(weeks=settings.LATEST_WEEK_THRESHOLD)

    df = pd.DataFrame.from_records(docs).sort_values("Publish Date", ascending=False)[:n]
    df['timestamp'] = df['Publish Date'].map(lambda x: datetime.strptime(x, settings.DATETIME_FORMAT))
    df.drop(df[df['timestamp'] < latest_datetime].index, inplace=True)
    return df.to_dict()


def db_get_hot_tenders(n: Union[int, None] = None) -> dict:
    """
        if n =None, get all related tenders
    """
    tenders = None
    # TODO: fetch n hot tenders, the rank
    # setattr(settings, 'HOT_TENDERS', tenders)


def db_get_expiring_tenders(n: Union[int, None] = None) -> dict:
    """
     if n =None, get all related tenders
    """
    tenders = None
    # TODO: fetch n expiring tenders, the rank
    # setattr(settings, 'HOT_TENDERS', tenders)

async def db_relax_search(n: Union[int, None] = None, words: list = None) -> dict:
    collection = mongo['tenders_client']['tenders']['open']
    relax_query_list = []
    for word in words:
        key = '(?i)' + word
        relx_query = {'$regex':key}
        relax_query_list.append({"Title":relx_query})
        relax_query_list.append({"Description":relx_query})
        relax_query_list.append({"Agency":relx_query})
    querys ={"$or":relax_query_list}
    limit = n
    docs = await do_relax_find(collection=collection, querys=querys, limit=limit)
    latest_datetime = datetime.now() - timedelta(weeks=settings.LATEST_WEEK_THRESHOLD)

    df = pd.DataFrame.from_records(docs).sort_values("Publish Date", ascending=False)[:n]
    df['timestamp'] = df['Publish Date'].map(lambda x: datetime.strptime(x, settings.DATETIME_FORMAT))
    df.drop(df[df['timestamp'] < latest_datetime].index, inplace=True)
    print(df)
    return df.to_dict()

async def do_find(collection: AsyncIOMotorCollection, condition: dict, skip: Union[int, None] = None,
                  limit: Union[int, None] = None,
                  sort: Union[dict, None] = None):
    tmp = []
    cursor = collection.find(condition)
    if sort:
        cursor.sort(sort)
    if skip:
        cursor.skip(skip)
    if limit:
        cursor.limit(limit)
    for doc in await cursor.to_list(1000):
        tmp.append(doc)

    return tmp

async def do_relax_find(collection: AsyncIOMotorCollection, querys: dict,
                    skip: Union[int, None] = None,
                    limit: Union[int, None] = None,
                    sort: Union[dict,None] = None):
    tmp = []
    cursor = collection.find(querys)
    if sort:
        cursor.sort(sort)
    if skip:
        cursor.skip(skip)
    if limit:
        cursor.limit(limit)
    for doc in await cursor.to_list(1000):
        tmp.append(doc)
    return tmp


#db_get_latest_tenders(10)

db_relax_search(n = 30,words=["Health","Agriculture"])


async def do_insert():
    pass

