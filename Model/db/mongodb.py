from urllib import parse
import pandas as pd
from pymongo import MongoClient
from database import SETTINGS
import logging
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
            # for col in df.columns:
            #     if 'date' in col:
            #         rows = self.database[df_name].find({col: {'$type': 2}})
            #         for row in rows:
            #             self.database[df_name].delete_one({col: row[col]})
            #             row[col] = datetime.datetime.strptime(row[col], "%Y-%m-%d")
            #             rows = self.database[df_name].save(row)
        except:
            logging.info(msg='Error happened during updating data')
            tmp_save.to_csv(f'backup/{datetime.datetime.now().date()}.csv')
            self.database[df_name].insert_many(tmp_save.to_dict(orient='records'))
        self.temp_save[df_name] = df