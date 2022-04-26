from datetime import datetime, timedelta
from config import settings
from typing import Union, Dict, List

from .engine import mongo


async def db_get_latest_tenders(n: int) -> list:
    """
    Get the latest tenders by querying the open date is within 8 weeks ago
    @param n: the number of tenders needing query
    @return: a list of tenders
    """
    client = mongo['tenders_client']
    db = client.get_default_database()

    collection = db['clean_grants_opened']
    date_range = datetime.now() - settings.LATEST_DATE_THRESHOLD
    cursor = collection.find({"open_date": {"$gt": date_range}},
                             {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
                              'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})
    if n != 0:
        cursor.limit(n)
    return await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_opened'])


def db_get_hot_tenders(n: Union[int, None] = None) -> Dict:
    """
        if n =None, get all related tenders
    """
    tenders = None
    # TODO: fetch n hot tenders, the rank
    # setattr(settings, 'HOT_TENDERS', tenders)


async def db_get_expiring_tenders(n: int) -> List:
    """
     if n =None, get all related tenders
    """

    client = mongo['tenders_client']
    db = client.get_default_database()
    collection = db['clean_grants_opened']
    date_range = datetime.now() + settings.LATEST_DATE_THRESHOLD
    cursor = collection.find({"close_date": {"$lt": date_range}},
                             {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
                              'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})
    if n != 0:
        cursor.limit(n)
    return await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_opened'])


async def db_get_tenders_by_keywords(keywords: str = None) -> List:
    """
    query all opened opportunities via divisions and tags
    @param divisions: a list of divisions which comes from
    @param tags: a list of tags
    @param limit: specify the limitation of the number of query
    @param skip: specify the offset when query
    @return: a list of opportunities
    """

    client = mongo['tenders_client']
    db = client.get_default_database()
    collection = db['clean_grants_opened']

    if keywords:
        cursor = collection.find(
            {"$text": {"$search": keywords, "$caseSensitive": False, "$diacriticSensitive": False}},
            {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
             'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1, "score": {"$meta": "textScore"}}).sort(
            [("score", {"$meta": "textScore"})])
    else:
        cursor = collection.find({}, {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
                                      'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})

    docs = await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_opened'])

    return docs


async def db_get_tenders_by_id(id_: str) -> Union[Dict, None]:
    """
    query tenders by id
    :param id_: the GO ID of each tenders
    :return: an tender object
    """

    client = mongo['tenders_client']
    db = client.get_default_database()
    collection = db['clean_grants_opened']
    return await collection.find_one({'GO ID': id_},
                                     {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
                                      'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})


async def db_get_tenders_by_ids(ids: list) -> list:
    """
    query tenders by id
    :param id_: the GO ID of each tenders
    :return: an tender object
    """
    if len(ids) == 0:
        return []

    client = mongo['tenders_client']
    db = client.get_default_database()
    collection = db['clean_grants_opened']
    cursor = collection.find({'GO ID': {'$in': ids}},
                             {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
                              'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})

    docs = await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_opened'])
    return docs


async def db_get_tenders_from_history(ids: list) -> list:
    """
    query tenders by id
    :param id_: the GO ID of each tenders
    :return: an tender object
    """
    if len(ids) == 0:
        return []

    client = mongo['tenders_client']
    db = client.get_default_database()
    collection = db['clean_grants_all']
    cursor = collection.find({'GO ID': {'$in': ids}},
                             {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
                              'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})

    docs = await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_opened'])
    return docs
