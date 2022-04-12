import pandas as pd
from conf.file_path import TENDERS_INFO_PATH, TENDERS_TAG_PATH, \
    TENDERS_TOPIC_PATH
from db.mongodb import MongoConx
from tenders.clean.data_clean import data_clean, convert_dtype
from tenders.features.lda_model import LDAModel
from tenders.features.tenders_feat_creator import TendersFeatCreator
from tenders.features.tenders_key_extractor import KeyExtractor


class TendersUpdater:
    def __init__(self, pk: str = 'id'):
        self.pk = pk
        self.mgx = MongoConx('tenders')
        self.raw_data_df = self.mgx.read_df('raw_grants_opened')
        self.raw_data_df['_id'] = self.raw_data_df['_id'].astype(str)
        self.raw_data_df['id'] = 'Grants' + self.raw_data_df['_id']

    def __reformat_key(self, row):
        row = row.dropna()
        return ' '.join(row[i] for i in row.index[1:])

    def __update_file(self, new_df, orig_path):
        orig_df = pd.read_csv(orig_path)
        orig_df.append(new_df).to_csv(orig_path, index=0)

    def __update_keys(self, new_info_df):
        ke = KeyExtractor()
        new_key_df = ke.get_tags(new_info_df, 'id', 'text')
        self.__update_file(new_key_df, TENDERS_TAG_PATH)
        return new_key_df

    def __update_topic(self, info_df):
        lda = LDAModel(info_df)
        lda.build_lda_model()
        new_topic_df = lda.get_tenders_topic()
        self.__update_file(new_topic_df, TENDERS_TOPIC_PATH)
        return new_topic_df

    def update_info(self, new_data_df):
        new_info_df = data_clean(new_data_df)
        self.__update_file(new_info_df, TENDERS_INFO_PATH)
        return new_info_df

    def update_opened(self, info_path=TENDERS_INFO_PATH, tag_path=TENDERS_TAG_PATH):
        '''

        Parameters
        ----------
        info_path
        tag_path

        Returns
        -------

        '''
        info_df = pd.read_csv(info_path)
        info_df = info_df[info_df['is_on'] == 1][['id', 'open_date', 'close_date', 'desc']]

        tag_df = pd.read_csv(tag_path)

        tag_df['tags'] = tag_df.apply(lambda x: self.__reformat_key(x), axis=1)
        info_df = info_df.merge(tag_df[['id', 'tags']], on='id')
        info_df['division'] = 'test'
        info_df = convert_dtype(info_df)
        info_df = info_df.merge(self.raw_data_df, on='id')
        info_df.fillna('', inplace=True)
        info_df = KeyExtractor.remove_stopword(info_df, 'desc')
        return info_df

    def update(self):
        '''

        Returns
        -------

        '''
        info_df = pd.read_csv(TENDERS_INFO_PATH)
        raw_remain_data_df = self.raw_data_df[~self.raw_data_df[self.pk].isin(info_df[self.pk])]

        if not raw_remain_data_df.empty:
            print(f'new Grants {raw_remain_data_df[self.pk].unique().tolist()}')
            # update info
            new_info_df = self.update_info(raw_remain_data_df)

            # update tag file
            self.__update_keys(new_info_df)

            # update topic file
            self.__update_topic(info_df)

            # update opened data
            new_open_info = self.update_opened()
            self.mgx.write_df(new_open_info, 'clean_grants_opened', True)

            # create mapping file
            tfc = TendersFeatCreator()
            tfc.create_all(self.pk)
            del raw_remain_data_df, new_info_df, new_open_info

        tag_df = pd.read_csv(TENDERS_TAG_PATH)
        tag_df = info_df[~info_df[self.pk].isin(tag_df[self.pk])]
        if not tag_df.empty:
            # update topic file
            self.__update_keys(tag_df)

            # update opened data
            new_open_info = self.__update_opened(raw_remain_data_df)
            self.mgx.write_df(new_open_info, 'clean_grants_opened', True)
            del tag_df, new_open_info

        topic_df = pd.read_csv(TENDERS_TOPIC_PATH)
        topic_df = info_df[~info_df[self.pk].isin(topic_df[self.pk])]
        if not topic_df.empty:
            # update topic file
            self.__update_topic(topic_df)
            del topic_df
