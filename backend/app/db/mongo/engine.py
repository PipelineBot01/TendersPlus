from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from urllib import parse

mongo = {
    'base_url': f'mongodb://{settings.MONGO_USERNAME}:{parse.quote(settings.MONGO_PASSWORD)}@{settings.MONGO_URL}'
}


async def init_db() -> None:
    """
    Initialize mongodb client
    @return: None
    """
    global mongo
    mongo['tenders_client'] = AsyncIOMotorClient(mongo['base_url'] + '/tenders')
    mongo['staff_client'] = AsyncIOMotorClient(mongo['base_url'] + '/staffs')

    # build searching index
    if 'clean_grants_opened_text_index' not in await mongo['tenders_client'].get_default_database().get_collection(
            'clean_grants_opened').index_information():
        await mongo['tenders_client'].get_default_database().get_collection('clean_grants_opened').create_index(
            [('title', 'text'), ('tags', 'text'), ('desc', 'text')], name='clean_grants_opened_text_index',
            weights={'title': 3, 'tags': 2, 'desc': 1})

    # count the records
    mongo['tenders_client_docs_count'] = {}
    mongo['tenders_client_docs_count']['clean_grants_opened'] = await mongo[
        'tenders_client'].get_default_database().get_collection('clean_grants_opened').count_documents({})
    print('opened tenders:', mongo['tenders_client_docs_count']['clean_grants_opened'])
