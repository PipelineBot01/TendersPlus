from urllib import parse
import pandas as pd
from pymongo import MongoClient
from db_conf import SETTINGS
import datetime


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

    def write_df(self, df: pd.DataFrame, df_name: str, overwrite=False):
        tmp_save = self.read_df(df_name)
        if overwrite:
            self.database[df_name].drop()
        try:
            self.database[df_name].insert_many(df.to_dict(orient='records'))
        except Exception as e:
            print(f'---- Error happened during updating data {e}')
            tmp_save.to_csv(f'error_backup_{datetime.datetime.now().date()}.csv', index=0)
            self.database[df_name].insert_many(tmp_save.to_dict(orient='records'))
        self.temp_save[df_name] = df
