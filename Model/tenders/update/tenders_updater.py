import pandas as pd

from conf.file_path import TENDERS_INFO_PATH, TENDERS_TAG_PATH, \
    TENDERS_TOPIC_PATH
from db.mongodb import MongoConx
from tenders.clean.data_clean import data_clean, update_opened_data
from tenders.features.lda_model import LDAModel
from tenders.features.tenders_feat_creator import TendersFeatCreator
from tenders.features.tenders_key_extractor import KeyExtractor


class Updater:
    def __init__(self, pk: str):
        self.pk = pk
        self.monx = MongoConx('tenders')

    def update_file(self, new_df, orig_path):
        orig_df = pd.read_csv(orig_path)
        orig_df.append(new_df).to_csv(orig_path)

    def update_is_open(self, opened_id):
        all_df = pd.read_csv(TENDERS_TAG_PATH)
        all_df[~all_df['id'].isin(opened_id), 'is_on'] = 0
        all_df[all_df['id'].isin(opened_id), 'is_on'] = 1

    def update(self):
        raw_data_df = self.monx.read_df('raw_grants_opened')
        info_df = self.monx.read_df('clean_train_info')[self.pk]

        raw_data_df[self.pk] = 'Grants' + raw_data_df['_id']
        raw_data_df = raw_data_df[~raw_data_df[self.pk].isin(info_df)]
        del info_df

        if not raw_data_df.empty:
            # update info file
            new_info_df = data_clean(raw_data_df)
            self.update_file(new_info_df, TENDERS_INFO_PATH)

            # update tag file
            ke = KeyExtractor()
            new_key_df = ke.get_tags(new_info_df, 'id', 'text')
            self.update_file(new_key_df, TENDERS_TAG_PATH)
            self.update_is_open(raw_data_df['id'])
            del ke, new_key_df

            # update topic file
            lda = LDAModel(pd.read_csv(TENDERS_INFO_PATH))
            lda.build_lda_model()
            new_topic_df = lda.get_topic(num_words=20)
            self.update_file(new_topic_df, TENDERS_TOPIC_PATH)
            del lda, new_topic_df, new_info_df

            # create mapping file
            tfc = TendersFeatCreator()
            tfc.create_tag_mapping('id')
            tfc.create_topic_mapping('id')

            # update opened data
            new_open_info = update_opened_data(TENDERS_TAG_PATH)
            self.monx.write_df(new_open_info, True)
