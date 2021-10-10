"""
the main.py is only used for testing chore codes
"""
import string

import pandas as pd, re, pickle, numpy as np
from Matcher.get_doc_vectors import get_d2v
from Matcher import Matcher
from Database.mongoDB import Mongo
from Matcher.data_preprocessor import doc_to_words_2
import Database.config as config

# ======= 1. connect to database ========
# connect to the "relevant" collection
tenders_db = Mongo(host=config.mongo_host,
                   port=config.mongo_port,
                   user=config.mongo_user,
                   pwd=config.mongo_pwd,
                   db=config.mongo_database_tenders,
                   collection=config.mongo_collection_relevant,
                   auth=True)

staffs_db = Mongo(host=config.mongo_host,
                  port=config.mongo_port,
                  user=config.mongo_user,
                  pwd=config.mongo_pwd,
                  db=config.mongo_database_staffs,
                  collection=config.mongo_collection_tag_lists,
                  auth=True)

# ======= 2. load matcher =========
d2v = get_d2v('Out/doc2vec-300.model')
matcher = Matcher(model=d2v, type='doc2vec')


# ======= 3. get a researcher information =========
researcher = staffs_db.collection.find_one({'Name': 'M. Selen Ayirtman Ercan'}, {'_id': 0})
tags = []
for k, v in researcher['ProjectTags_Weight'].items():
    # print(k, v.strip(string.punctuation))
    if int(v.strip(string.punctuation)) == 100:
        tags.append(k)
tags = ' '.join(tags)
tags = doc_to_words_2(tags)
tags = set(tags)
print("researcher's tags\n", tags)
print()


# ======= 4. match the researcher tags with tenders =========
matched_tenders = matcher.match(tags, 30)
print('matched_tenders\n', matched_tenders)
print()


# ======= 5. filter out those matched tenders that are irrelevant to researcher =======
filter_tenders = []
for t in matched_tenders:
    has = tenders_db.collection.find_one({'ATM ID': t[0]})
    if has:
        filter_tenders.append(t)
print('filter_tenders:\n', filter_tenders)
