"""
********** <[ STEP 1st ]> **********

What to do:
- data_loader will load the data from remote database,
  then we can pass them to the preprocessor or we can just save them into history_tenders

Authors:
- Yuxuan Yang u7078049

"""

from Database.mongoDB import Mongo
from Database import config
import pandas as pd, pickle


def load():
    database = Mongo(host=config.mongo_host,
                     port=config.mongo_port,
                     user=config.mongo_user,
                     pwd=config.mongo_pwd,
                     db=config.mongo_database_tenders,
                     collection=config.mongo_collection_all,
                     auth=True)

    data = pd.DataFrame.from_dict(
        database.collection.find({}, {"Title": 1, "_id": 0, 'Category': 1, 'Description': 1, 'ATM ID': 1}),
        orient='columns')
    print(data.head())
    with open('../Out/history_tenders_unprocessed', 'wb') as f:
        pickle.dump(data, f)

    return data


if __name__ == '__main__':
    load()
