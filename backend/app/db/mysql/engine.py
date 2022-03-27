from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings

# 1. create engine
engine = create_engine(
    f'mysql+pymysql://{settings.MYSQL_USERNAME}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_URL}/{settings.MYSQL_DATABASE}',
pool_recycle=3600
)

# 2. build session
session = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, autocommit=False)

# 3. create orm entry
base = declarative_base()
