"""
this script is used for removing tenders that doesn't meet out requirement
"""

from Database.mongoDB import Mongo
import Database.config as config
import nltk

# ======== connect to databse =========
db = Mongo(host=config.mongo_host,
           port=config.mongo_port,
           user=config.mongo_user,
           pwd=config.mongo_pwd,
           db=config.mongo_database_tenders,
           collection=config.mongo_collection_test_ryan)

# ======== remove tenders that description less than 20 words =========
words_threshold = 20
data = db.find_all(show_id=True)
for i in data:
    if 'Description' in i:
        desc = i['Description']
        words = nltk.word_tokenize(desc)
        if len(words) < words_threshold:
            db.collection.delete_one({'_id': i['_id']})
    else:
        db.collection.delete_one({'_id': i['_id']})
