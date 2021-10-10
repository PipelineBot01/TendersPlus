"""
This script is used to extract keywords from description of each tender
"""

from Database.mongoDB import Mongo
import Database.config as config
from keybert import KeyBERT

# ============= load keybert model =================
model = KeyBERT('all-mpnet-base-v2')


database = Mongo(host=config.mongo_host,
                 port=config.mongo_port,
                 user=config.mongo_user,
                 pwd=config.mongo_pwd,
                 db=config.mongo_database_tenders,
                 collection=config.mongo_collection_test_ryan,
                 auth=True)

# ======= load all the tenders ==============
data = database.collection.find({}, {'_id': 1, 'Description': 1})

for i in data:
    if 'Description' in i:
        doc = i['Description']
        words = model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
        word_weight = {j[0]: j[1] for j in words}
        database.collection.update_one({'_id': i['_id']}, {"$set": {'Keywords': word_weight}})
