from datetime import datetime, timedelta
from config import settings
from typing import Union, Dict, List

from .engine import mongo


async def db_get_latest_tenders(l: int = 0, s: int = 0) -> list:
    """
    Get the latest tenders by querying the open date is within 8 weeks ago
    @param n: the number of tenders needing query
    @return: a list of tenders
    """

    date_range = datetime.now() - settings.LATEST_DATE_THRESHOLD
    cursor = mongo['collection_clean_grants_all'].find({"open_date": {"$gt": date_range}},
                                                              {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1,
                                                               'Close Date & Time': 1,
                                                               'Publish Date': 1, 'Location': 1, 'tags': 1,
                                                               'division': 1})
    if l != 0:
        cursor.limit(l)
    if s != 0:
        cursor.skip(s)
    return await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_all'])


async def db_get_expiring_tenders(l: int = 0, s: int = 0) -> List:
    """
     if n =None, get all related tenders
    """
    date_range = datetime.now() + settings.EXPIRING_DATE_THRESHOLD
    cursor = mongo['collection_clean_grants_all'].find(
        {"close_date": {'$gt': datetime.now(), "$lt": date_range}},
        {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
         'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})

    if l != 0:
        cursor.limit(l)
    if s != 0:
        cursor.skip(s)

    return await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_all'])


async def db_get_tenders_by_keywords(keywords: str = None, l: int = 0, s: int = 0) -> List:
    """
    query all opened opportunities via divisions and tags
    @param divisions: a list of divisions which comes from
    @param tags: a list of tags
    @param limit: specify the limitation of the number of query
    @param skip: specify the offset when query
    @return: a list of opportunities
    """

    collection = mongo['collection_clean_grants_all']

    if keywords:
        cursor = collection.find(
            {"$text": {"$search": keywords, "$caseSensitive": False, "$diacriticSensitive": False}},
            {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
             'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1, "score": {"$meta": "textScore"}}).sort(
            [("score", {"$meta": "textScore"})])
    else:
        cursor = collection.find({}, {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
                                      'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})

    if l != 0:
        cursor.limit(l)
    if s != 0:
        cursor.skip(s)

    docs = await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_all'])

    return docs


async def db_get_tenders_from_history_by_id(id_: str) -> Union[Dict, None]:
    """
    query tenders by id
    :param id_: the GO ID of each tenders
    :return: an tender object
    """


    return await mongo['collection_clean_grants_all'].find_one({'GO ID': id_},
                                     {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
                                      'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})


async def db_get_tenders_from_opened_by_ids(ids: list) -> list:
    """
    query tenders by id
    :param id_: the GO ID of each tenders
    :return: an tender object
    """
    if len(ids) == 0:
        return []


    cursor = mongo['collection_clean_grants_all'].find({'GO ID': {'$in': ids}},
                             {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
                              'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})

    docs = await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_all'])
    return docs


async def db_get_tenders_from_history_by_ids(ids: list) -> list:
    """
    query tenders by id
    :param id_: the GO ID of each tenders
    :return: an tender object
    """
    if len(ids) == 0:
        return []

    cursor = mongo['collection_clean_grants_all'].find({'GO ID': {'$in': ids}},
                             {'_id': 0, 'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
                              'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})

    docs = await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_all'])
    return docs
