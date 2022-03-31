from urllib import parse
import pandas as pd
from pymongo import MongoClient
from database import SETTINGS


class MongoConx:
    def __init__(self, database, conf=SETTINGS, auth=True):
        self.uri = f'mongodb://{conf["user"]}:{parse.quote(conf["pwd"])}@{conf["host"]}:{conf["port"]}/{database}'
        self.database = MongoClient(self.uri)[database] if auth else MongoClient(host=conf['host'], port=conf['port'])[
            database]
        self.temp_save = {}

    def read_df(self, df_name) -> pd.DataFrame:
        if df_name in self.temp_save.keys():
            return self.temp_save[df_name]
        data = pd.DataFrame([i for i in self.database[df_name].find({})])
        self.temp_save[df_name] = data
        return data

    def write_df(self, df, df_name, overwrite=False):
        if overwrite:
            self.database[df_name].drop()
        self.database[df_name].insert_many(df.to_dict(orient='records'))
        self.temp_save[df_name] = df

