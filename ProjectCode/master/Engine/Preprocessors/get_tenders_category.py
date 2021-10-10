"""
get all tenders categories

Authors:
- Yuxuan Yang u7078049
"""

from Database.mongoDB import Mongo
import Database
import pandas as pd

db = Mongo(host=Database.Mongo.config.mongo_host,
           port=Database.Mongo.config.mongo_port,
           user=Database.Mongo.config.mongo_user,
           pwd=Database.Mongo.config.mongo_pwd,
           db=Database.Mongo.config.mongo_database,
           collection=Database.Mongo.config.mongo_collection)

tenders_categories = {}
for i in db.find({},{'_id':0,'Category':1}):
    try:
        tmp = i['Category'].split('-')
        tenders_categories[tmp[0].strip()]=tmp[1].strip()
    except:
        pass
df = pd.DataFrame.from_dict(tenders_categories,orient='index',columns=['Category'])


with  pd.ExcelWriter(path='../Out/tenders_categories.xlsx') as writer:
    df.to_excel(writer,sheet_name='sheet1',encoding='utf8')