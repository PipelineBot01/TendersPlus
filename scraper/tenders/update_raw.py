import pandas as pd

from db.mongoDB import mongo
from go_conf import mongo_host, mongo_port, username, passwd, database_name


def update_raw_all():
    db = mongo(mongo_host, mongo_port, username, passwd, database_name, "raw_grants_opened")
    db.use_database('raw_grants_opened')
    open_df = pd.DataFrame(db.find_all())
    new_url = open_df['URL']

    db.use_database('raw_grants_all')
    old_df_urls = db.find_col('URL')
    old_url = pd.DataFrame(old_df_urls)
    new_data_dict = open_df.T.to_dict()
    update_URL_list = list(pd.merge(new_url, old_url)['URL'])

    update_set = set(update_URL_list)
    update_count = 0
    insert_count = 0
    for j in new_data_dict:
        url = new_data_dict[j]["URL"]
        if url in update_set:
            q = {'URL': url}
            v = {'$set': new_data_dict[j]}
            update_count = update_count + 1
            db.update_one(q, v)
        else:
            insert_count = insert_count + 1
            db.insert(new_data_dict[j])
    print('update ' + str(update_count) + ' records')
    print('insert ' + str(insert_count) + ' records')
