from pymongo import MongoClient
from urllib import parse

# mongo database
class Mongo:
    def __init__(self, host='localhost', port='27017', user=None, pwd=None, db='test', collection='test', auth=True):
        """init MongoDB and connection

        :param host:
        :param port:
        :param db:
        :param collection:
        :param auth: if auth is true, then we need username and password to connect to the database
        """
        if auth:
            passwd = parse.quote(pwd)
            uri = 'mongodb://' + user + ':' + passwd + '@' + host + ':' + port + '/' + db
            client = MongoClient(uri)
        else:
            client = MongoClient(host=host, port=port)

        self.db = client[db]  # database
        self.collection = self.db[collection]  # table

        if db not in client.list_database_names():
            print("no such database!")
        if collection not in self.db.list_collection_names():
            print("no such collection！")

    def __str__(self):
        """database ifo"""
        db = self.db.name
        collection = self.collection.name
        num = self.collection.find().count()
        return "databese:{}, collection:{}, has:{} records".format(db, collection, num)

    def __len__(self):
        """records numbers"""
        return self.collection.find().count()

    def count(self):
        """database numbers"""
        return len(self)

    def insert(self, *args, **kwargs):
        """insert one or many records

        :param args: multi data list(dict)/ dict/ tuple(dict)
        :param kwargs: simple data  name = 'A', age = '20'
        :return: _id
        """
        documents = []
        for i in args:
            if isinstance(i, dict):
                documents.append(i)
            else:
                documents += [x for x in i]
        if kwargs:
            documents.append(kwargs)
        return self.collection.insert_many(documents)

    def delete(self, *args, **kwargs):
        """delete one or more records

        :param args: dict, exmaple {"gender": "male"}
        :param kwargs: attribute，example gender="male"
        :return: delete numbers
        """

        list(map(kwargs.update, args))
        result = self.collection.delete_many(kwargs)
        return result.deleted_count

    def update(self, *args, **kwargs):
        """updata one or more records

        :param args: dict:{"author":"XerCis"}，list[_id]:[{'_id': ObjectId('1')}, {'_id': ObjectId('2')}]
        :param kwargs: attribute to be updated，country="China", age=22
        :return: update records numbers
        """
        value = {"$set": kwargs}
        query = {}
        n = 0
        list(map(query.update, list(filter(lambda x: isinstance(x, dict), args))))
        for i in args:
            if not isinstance(i, dict):
                for id in i:
                    query.update(id)
                    result = self.collection.update_one(query, value)
                    n += result.modified_count
        result = self.collection.update_many(query, value)
        return n + result.modified_count

    def find(self, *args, **kwargs):
        """
        pymongo find API
        """
        return self.collection.find(*args, **kwargs)

    def find_all(self, show_id=False):
        """find all records

        :param show_id: display _id or not, default False
        :return: all records
        """
        if show_id == False:
            return [i for i in self.collection.find({}, {"_id": 0})]
        else:
            return [i for i in self.collection.find({})]

    def find_col(self, *args, **kwargs):
        """find some attributes

        :param key: "name","age"
        :param value: gender="male"
        :return:
        """
        key_dict = {"_id": 0}  # not show _id
        key_dict.update({i: 1 for i in args})
        return [i for i in self.collection.find(kwargs, key_dict)]

