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
    if 'clean_grants_opened_text_index' in await mongo['tenders_client'].get_default_database().get_collection(
            'clean_grants_opened').index_information():
        await mongo['tenders_client'].get_default_database().get_collection('clean_grants_opened').drop_index(
            index_or_name='clean_grants_opened_text_index')

    await mongo['tenders_client'].get_default_database().get_collection('clean_grants_opened').create_index(
        [('Title', 'text'), ('desc', 'text'), ('Primary Category', 'text'), ('GO ID', 'text')],
        name='clean_grants_opened_text_index',
        weights={'Title': 3, 'desc': 2, 'GO ID': 1})

    # count the records
    mongo['tenders_client_docs_count'] = {}
    mongo['tenders_client_docs_count']['clean_grants_opened'] = await mongo[
        'tenders_client'].get_default_database().get_collection('clean_grants_opened').count_documents({})
    print('opened tenders:', mongo['tenders_client_docs_count']['clean_grants_opened'])
