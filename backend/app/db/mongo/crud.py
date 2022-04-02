from datetime import datetime, timedelta
from config import settings
from typing import Union

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
    cursor = collection.find({"open_date": {"$gt": date_range}}, {'_id': 0, 'desc': 0, 'Selection Process': 0})
    if n != 0:
        cursor.limit(n)
    return await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_opened'])


def db_get_hot_tenders(n: Union[int, None] = None) -> dict:
    """
        if n =None, get all related tenders
    """
    tenders = None
    # TODO: fetch n hot tenders, the rank
    # setattr(settings, 'HOT_TENDERS', tenders)


async def db_get_expiring_tenders(n: int) -> list:
    """
     if n =None, get all related tenders
    """

    client = mongo['tenders_client']
    db = client.get_default_database()
    collection = db['clean_grants_opened']
    date_range = datetime.now() + settings.LATEST_DATE_THRESHOLD
    cursor = collection.find({"close_date": {"$lt": date_range}}, {'_id': 0, 'desc': 0, 'irf_id': 0})
    if n != 0:
        cursor.limit(n)
    return await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_opened'])


async def db_get_opportunities(keywords: str = None) -> list:
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
        cursor = collection.find({"$text": {"$search": keywords, "$caseSensitive":False,"$diacriticSensitive":False}},
                                 {'_id': 0, 'id': 0, 'desc': 0, 'irf_id': 0, "score": {"$meta": "textScore"}}).sort(
            [("score", {"$meta": "textScore"})])
    else:
        cursor = collection.find({}, {'Title': 1, 'URL': 1, 'GO ID': 1, 'Agency': 1, 'Close Date & Time': 1,
                                      'Publish Date': 1, 'Location': 1, 'tags': 1, 'division': 1})

    docs = await cursor.to_list(length=mongo['tenders_client_docs_count']['clean_grants_opened'])

    return docs

# async def db_relax_search(n: Union[int, None] = None, words: list = None) -> dict:
#     collection = mongo['tenders_client']['tenders']['open']
#     relax_query_list = []
#     for word in words:
#         key = '(?i)' + word
#         relx_query = {'$regex':key}
#         relax_query_list.append({"Title":relx_query})
#         relax_query_list.append({"Description":relx_query})
#         relax_query_list.append({"Agency":relx_query})
#     querys ={"$or":relax_query_list}
#     limit = n
#     docs = await do_relax_find(collection=collection, querys=querys, limit=limit)
#     latest_datetime = datetime.now() - timedelta(weeks=settings.LATEST_WEEK_THRESHOLD)
#
#     df = pd.DataFrame.from_records(docs).sort_values("Publish Date", ascending=False)[:n]
#     df['timestamp'] = df['Publish Date'].map(lambda x: datetime.strptime(x, settings.DATETIME_FORMAT))
#     df.drop(df[df['timestamp'] < latest_datetime].index, inplace=True)
#     print(df)
#     return df.to_dict()

# async def do_find(collection: AsyncIOMotorCollection, condition: dict, skip: Union[int, None] = None,
#                   limit: Union[int, None] = None,
#                   sort: Union[dict, None] = None):
#     tmp = []
#     cursor = collection.find(condition)
#     if sort:
#         cursor.sort(sort)
#     if skip:
#         cursor.skip(skip)
#     if limit:
#         cursor.limit(limit)
#     for doc in await cursor.to_list(1000):
#         tmp.append(doc)
#
#     return tmp
#
# async def do_relax_find(collection: AsyncIOMotorCollection, querys: dict,
#                     skip: Union[int, None] = None,
#                     limit: Union[int, None] = None,
#                     sort: Union[dict,None] = None):
#     tmp = []
#     cursor = collection.find(querys)
#     if sort:
#         cursor.sort(sort)
#     if skip:
#         cursor.skip(skip)
#     if limit:
#         cursor.limit(limit)
#     for doc in await cursor.to_list(1000):
#         tmp.append(doc)
#     return tmp


# db_get_latest_tenders(10)

# db_relax_search(n=30, words=["Health", "Agriculture"])
