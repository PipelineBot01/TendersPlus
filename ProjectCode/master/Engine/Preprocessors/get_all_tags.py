"""
This script is used to get all the tags from all staffs, and do some text process: remove stop words, lowercase, lemmatize

"""

from Database.mongoDB import Mongo
import Database.config  as config
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

lemmatize = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
database = Mongo(host=config.mongo_host,
                 port=config.mongo_port,
                 user=config.mongo_user,
                 pwd=config.mongo_pwd,
                 db=config.mongo_database_staffs,
                 collection='tags_of_staffs',
                 auth=True)

data =  database.collection.find({},{'_id':0,'Tags':1})
all_tags = [ i['Tags'] for i in data]


# =========== process tags============
tags = [ t.lower() for t in all_tags]
with open('../Out/researcher_tags.txt', 'w',encoding='utf8') as f:
    for t in tags:
        f.write(f'{t}\n')
print(len(all_tags))
