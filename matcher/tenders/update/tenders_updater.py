import os
import pandas as pd
from conf.clean import REMAIN_COLS
from conf.file_path import TENDERS_INFO_PATH, TENDERS_TAG_PATH, \
    TENDERS_TOPIC_PATH, TENDERS_CATE_DIV_MAP_PATH, TENDERS_RELATION_MAP_PATH, TENDERS_EMAIL_PATH
from db.mongodb import MongoConx
from tenders.clean.data_clean import data_clean, convert_dtype
from tenders.features.lda_model import LDAModel
from tenders.features.tenders_feat_creator import TendersFeatCreator
from tenders.features.tenders_key_extractor import KeyExtractor
from tenders.matching.tenders_relation import TendersMatcher


class TendersUpdater:
    def __init__(self,
                 info_path=TENDERS_INFO_PATH,
                 tag_path=TENDERS_TAG_PATH,
                 topic_path=TENDERS_TOPIC_PATH,
                 cate_div_map=TENDERS_CATE_DIV_MAP_PATH,
                 tenders_email_path=TENDERS_EMAIL_PATH,
                 pk: str = 'id'):
        self.pk = pk
        self.info_path = info_path
        self.tag_path = tag_path
        self.topic_path = topic_path
        self.cate_div_map = cate_div_map
        self.tenders_email_path = tenders_email_path
        self.mgx = MongoConx('tenders')
        self.raw_data_df = None

    def __check_quality(self, raw_data: pd.DataFrame, key_id='GO ID') -> pd.DataFrame:
        assert len(raw_data[raw_data[key_id].isna()]) / len(
            raw_data) < 0.1, f'---- contains over 10% grants with missing {key_id}'
        n_dup = len(raw_data.duplicated([key_id]))
        if n_dup > 0:
            print(f'---- contains {n_dup} duplicated grants')
        return raw_data.drop_duplicates(key_id, keep='first')

    def __reformat_key(self, row):
        row = row.dropna()
        return ' '.join(row[i] for i in row.index[1:])

    def __update_file(self, new_df, orig_path):
        if os.path.exists(orig_path):
            orig_df = pd.read_csv(orig_path)
            orig_df.append(new_df).to_csv(orig_path, index=0)
        else:
            new_df.to_csv(orig_path, index=0)

    def __update_keys(self, new_info_df):
        ke = KeyExtractor()
        new_key_df = ke.get_tags(new_info_df, pk=self.pk, text_col='text')
        self.__update_file(new_key_df, self.tag_path)
        return new_key_df

    def __update_topic(self, info_df):
        lda = LDAModel(info_df)
        lda.build_lda_model()
        new_topic_df = lda.get_tenders_topic()
        self.__update_file(new_topic_df, self.topic_path)
        return new_topic_df

    def update_info(self, new_data_df, overwrite=False):
        new_info_df = data_clean(new_data_df, overwrite)
        self.__update_file(new_info_df, self.info_path)

        return new_info_df

    def __create_index(self, collection):
        collection.create_index(
            [('Title', 'text'), ('desc', 'text'), ('Primary Category', 'text'), ('GO ID', 'text')],
            name='clean_grants_opened_text_index', weights={'Title': 3, 'desc': 2, 'GO ID': 1})
        # build hash index
        collection.create_index([('GO ID', 'hashed')], name='clean_grants_opened_hash_index')

    def update_opened(self) -> pd.DataFrame:
        '''

        Parameters
        ----------
        info_path
        tag_path

        Returns
        -------

        '''
        info_df = pd.read_csv(self.info_path)
        info_df = info_df[[self.pk, 'open_date', 'close_date', 'desc', 'category', 'sub_category']]

        tag_df = pd.read_csv(self.tag_path)
        tag_df['tags'] = tag_df.apply(lambda x: self.__reformat_key(x), axis=1)
        info_df = info_df.merge(tag_df[[self.pk, 'tags']], on=self.pk)
        cate_df = info_df[[self.pk, 'category', 'sub_category']].melt(id_vars=self.pk
                                                                      ).dropna()[[self.pk, 'value']].rename(
            columns={'value': 'category'})
        cate_div_map_df = self.__update_cate_div_map(cate_df)
        cate_div_map_df.to_csv(self.cate_div_map, index=0)

        cate_df = cate_df.merge(cate_div_map_df, how='left')
        cate_df.drop_duplicates([self.pk, 'division'], inplace=True)
        cate_df = cate_df.groupby(self.pk)['division'].apply(lambda x: '/'.join(i for i in x)).reset_index()
        info_df = info_df.merge(cate_df)

        info_df = convert_dtype(info_df)
        info_df = info_df.merge(self.raw_data_df, on=self.pk)
        info_df.fillna('', inplace=True)
        info_df = KeyExtractor.remove_stopword(info_df, 'desc')
        return info_df

    # TODO: only for testing
    def __update_all(self):
        all_df = self.mgx.read_df_by_cols('raw_grants_all', REMAIN_COLS)
        info_df = data_clean(all_df)
        tag_df = pd.read_csv(self.tag_path)
        tag_df['tags'] = tag_df.apply(lambda x: self.__reformat_key(x), axis=1)
        info_df = info_df.merge(tag_df[[self.pk, 'tags']], on=self.pk)
        cate_map_df = pd.read_csv(self.cate_div_map)
        cate_df = info_df[[self.pk, 'category', 'sub_category']].melt(
            id_vars=self.pk).dropna()[[self.pk, 'value']].rename(columns={'value': 'category'})
        cate_df = cate_df.merge(cate_map_df, how='left')
        cate_df.drop_duplicates([self.pk, 'division'], inplace=True)
        cate_df = cate_df.groupby(self.pk)['division'].apply(lambda x: '/'.join(i for i in x)).reset_index()
        info_df = info_df.merge(cate_df)
        info_df = convert_dtype(info_df)
        info_df = info_df.merge(all_df, left_on='go_id', right_on='GO ID')
        info_df.fillna('', inplace=True)
        info_df = KeyExtractor.remove_stopword(info_df, 'desc')
        self.mgx.write_df(info_df, 'clean_grants_all', True)

    def __keyword_error_checking(self, info_df):
        keyword_df = pd.read_csv(self.tag_path)
        remain_df = info_df[~info_df[self.pk].isin(keyword_df[self.pk])]
        if not remain_df.empty:
            print(f'-- fixing missing keyword data {remain_df[self.pk].unique().tolist()}')
            self.__update_keys(remain_df)
            tfc = TendersFeatCreator()
            tfc.create_tag_mapping(self.pk)
            print('-- fixing end')
            return True
        return False

    def __topic_error_checking(self, info_df):
        topic_df = pd.read_csv(self.topic_path)
        remain_df = info_df[~info_df[self.pk].isin(topic_df[self.pk])]
        if not remain_df.empty:
            print('-- fixing missing topic data')
            self.__update_topic(remain_df)
            tfc = TendersFeatCreator()
            tfc.create_topic_mapping(self.pk)
            print('-- fixing end')
            return True
        return False

    def __update_cate_div_map(self, cate_df):
        cate_div_map_df = pd.read_csv(self.cate_div_map)
        cate_div_map_df = cate_div_map_df[~cate_div_map_df['division'].isin(['OTHERS RELEVANT',
                                                                             'OTHERS IRRELEVANT'])].drop_duplicates()
        new_div_df = cate_df[~cate_df['category'].isin(cate_div_map_df['category'])]
        if not new_div_df.empty:
            print(f'---- new category {new_div_df["category"].unique().tolist()}')
            tm = TendersMatcher()
            tmp_df = pd.DataFrame()
            for t_id in new_div_df[self.pk].unique():
                result_df = tm.match(t_id).merge(cate_df, on=self.pk).merge(cate_div_map_df, on='category')
                result_df = result_df.groupby('division')[self.pk].count().reset_index().rename(columns={self.pk:
                                                                                                         'cnt'})
                result_df = result_df.sort_values('cnt', ascending=False)[:min(3, len(result_df))]
                result_df['tmp'] = 1
                orig_df = new_div_df[new_div_df[self.pk] == t_id].copy()
                orig_df['tmp'] = 1
                orig_df = orig_df.merge(result_df, on='tmp')
                tmp_df = tmp_df.append(orig_df)
            tmp_df = tmp_df.groupby(['division',
                                     'category'])['cnt'].sum().reset_index().sort_values('cnt', ascending=False)
            tmp_df = tmp_df.groupby(['category']).head(3)
            cate_div_map_df = cate_div_map_df.append(tmp_df.drop('cnt', axis=1))
        return cate_div_map_df
    
    def __get_opened(self):
        print('-- start getting opened tenders info')
        self.raw_data_df = self.mgx.read_df_by_cols('raw_grants_opened', REMAIN_COLS)
        self.raw_data_df = self.__check_quality(self.raw_data_df)
        self.raw_data_df['GO ID'] = self.raw_data_df['GO ID'].astype(str)
        self.raw_data_df[self.pk] = 'Grants' + self.raw_data_df['GO ID']
        print('-- end getting opened tender info')
    
    def update_relation_map(self):
        tm = TendersMatcher()
        info_df = pd.read_csv(self.info_path)[['id']]
        size = len(info_df)
        tmp_dict = pd.DataFrame()
        for index, row in info_df.iterrows():
            result_df = tm.match(row['id'])
            result_df['orig_id'] = row['id']
            tmp_dict = tmp_dict.append(result_df)
            print(f'---- complete {index}/{size}')
        tmp_dict.to_csv(TENDERS_RELATION_MAP_PATH, index=0)
    
    def update(self):
        '''

        Returns
        -------

        '''
        print('<start updating tenders files>')

        self.__get_opened()

        if os.path.exists(self.info_path):
            info_df = pd.read_csv(self.info_path)
            raw_remain_data_df = self.raw_data_df[~self.raw_data_df[self.pk].isin(info_df[self.pk])]
            overwrite = False
        else:
            old_raw_data_df = self.mgx.read_df_by_cols('raw_grants_all', REMAIN_COLS)
            old_raw_data_df[self.pk] = 'Grants' + old_raw_data_df['GO ID']
            old_raw_data_df = old_raw_data_df[~old_raw_data_df['GO ID'].isin(self.raw_data_df['GO ID'].unique())]
            raw_remain_data_df = old_raw_data_df.append(self.raw_data_df)
            del old_raw_data_df
            overwrite = True

        if not os.path.exists(self.tenders_email_path):
            pd.DataFrame({'go_id': []}).to_csv(self.tenders_email_path, index=0)

        if not raw_remain_data_df.empty:
            print(f'-- {len(raw_remain_data_df)} new Grants {raw_remain_data_df[self.pk].unique().tolist()}')

            # update new email tenders
            print('-- start updating email tenders')
            tmp_new_df = pd.read_csv(self.tenders_email_path)
            tmp_new_df.append(raw_remain_data_df[['GO ID']].rename(columns={'GO ID': 'go_id'}
                                                                   )).to_csv(self.tenders_email_path, index=0)
            print('-- end updating email tenders')

            # update info
            print('-- start updating tender info')
            new_info_df = self.update_info(raw_remain_data_df, overwrite)
            print('-- end updating tender info')

            # update tag file
            print('-- start updating tender keyword')
            self.__update_keys(new_info_df)
            print('-- end updating tender keyword')

            # update topic file
            print('-- start updating tender topic')
            self.__update_topic(new_info_df)
            print('-- end updating tender topic')

            # update opened data
            print('-- start updating opened opportunities')
            new_open_info = self.update_opened()
            self.mgx.write_df(new_open_info, 'clean_grants_opened', True)
            self.__create_index(self.mgx.database['clean_grants_opened'])
            print('-- end updating opened opportunities')

            # create mapping file
            print('-- start updating tenders mapping files')
            tfc = TendersFeatCreator()
            tfc.create_all(self.pk)
            print('-- end updating tenders mapping files')
            del raw_remain_data_df, new_info_df, new_open_info

            print('-- start updating tenders relation')
            self.update_relation_map()
            print('-- end updating tenders relation')

        info_df = pd.read_csv(self.info_path)
        error_1 = self.__keyword_error_checking(info_df)
        error_2 = self.__topic_error_checking(info_df)

        if error_1 or error_2:
            print('-- fixing missing opened data')
            new_open_info = self.update_opened()
            self.mgx.write_df(new_open_info, 'clean_grants_opened', True)
            self.__create_index(self.mgx.database['clean_grants_opened'])
            print('-- fixing end')

            print('-- fixing updating tenders relation')
            self.update_relation_map()
            print('-- fixing updating tenders relation')

        # TODO: only for testing
        print('-- start updating all grants info')
        self.__update_all()
        self.__create_index(self.mgx.database['clean_grants_all'])
        print('-- end updating all grants info')

        print('<end updating tenders files>')
