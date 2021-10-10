import pandas as pd,pickle
from Database.mongoDB import Mongo
from Database import config

# # this file is used to extract tenders description which category is marked as 2（not sure if related to researcher）
# df = pd.read_excel('../Out/tenders_categories.xlsx', sheet_name='sheet1')
# print()
# c = df.columns[2]
# unknown_categories = df[df[c] == 2]
# unknown_categories = unknown_categories['Category']
#
# d = {}
# for i in unknown_categories:
#     d[i] = []
# print(len(d))
#
# database = Mongo(host=config.mongo_host,
#                  port=config.mongo_port,
#                  user=config.mongo_user,
#                  pwd=config.mongo_pwd,
#                  db=config.mongo_database_tenders,
#                  collection=config.mongo_collection_all,
#                  auth=True)
# data = pd.DataFrame.from_dict(
#         database.collection.find({}, {"Title": 1, "_id": 0, 'Category': 1, 'Description': 1, 'ATM ID': 1}),
#         orient='columns')
#
#
#
# data = data[data['Category'].isin(unknown_categories)]
# for r in data.itertuples():
#     # print(r)
#     d[r[3]].append(r[4])



# for i in data:
#     print(i)
#     d[i['Category']].append(i['Description'])

# print(len(d))
# with open('data','wb') as f:
#     pickle.dump(d,f)

with open('data','rb') as f:
    d = pickle.load(f)
print(d)
new_data = pd.DataFrame.from_dict(d,orient='index')
with pd.ExcelWriter('../Out/tenders_categories_unknown.xlsx') as writer:
    new_data.to_excel(writer, sheet_name='sheet1')

# # print(unknown_categories)
