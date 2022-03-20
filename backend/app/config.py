from pydantic import BaseSettings
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--env_path', type=str, action='store')
env_path = parser.parse_args().env_path

if env_path is None:
    env_path = './.env'


class Settings(BaseSettings):
    # nosql server
    MONGO_URL: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str

    # mysql server
    MYSQL_USERNAME:str
    MYSQL_PASSWORD:str
    MYSQL_URL:str
    MYSQL_DATABASE:str

    # use to filter out tenders
    EXPIRING_WEEK_THRESHOLD: int = 1
    LATEST_WEEK_THRESHOLD: int = 8
    HOT_THRESHOLD: str = ''

    # app server
    APP_HOST: str = 'localhost'
    APP_PORT: int = 202202
    DATETIME_FORMAT = '%d-%b-%Y'

    LATEST_TENDERS: dict = None
    HOT_TENDERS:dict =None


settings = Settings(_env_file=env_path)
