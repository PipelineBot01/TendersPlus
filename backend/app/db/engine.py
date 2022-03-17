from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from urllib import parse

mongo = {
    'base_url': f'mongodb://{settings.MONGO_USERNAME}:{parse.quote(settings.MONGO_PASSWORD)}@{settings.MONGO_URL}'
}


def init_db() -> AsyncIOMotorClient:
    global mongo
    mongo['tenders_client'] = AsyncIOMotorClient(mongo['base_url'] + '/tenders')

