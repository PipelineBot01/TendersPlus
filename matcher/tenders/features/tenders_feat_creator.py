import re
import pandas as pd
from conf.file_path import TENDERS_TAG_PATH, TENDERS_TAG_MAP_PATH, TENDERS_TOPIC_PATH, TENDERS_TOPIC_MAP_PATH


class TendersFeatCreator:

    def __init__(self,
                 tag_path=TENDERS_TAG_PATH,
                 tag_map_path=TENDERS_TAG_MAP_PATH,
                 topic_path=TENDERS_TOPIC_PATH,
                 topic_map_path=TENDERS_TOPIC_MAP_PATH):

        self.tag_path = tag_path
        self.tag_map_path = tag_map_path
        self.topic_path = topic_path
        self.topic_map_path = topic_map_path

    def __get_topic(self, row):
        re_rule = r'\((.*?)\)'
        topic_list = re.findall(re_rule, row['topics'])
        return topic_list

    def __split_topic(self, row):
        result = row['values'].split(',')
        print(result)
        row['topic'] = result[0]
        row['weight'] = result[1]
        return row

    def create_tag_mapping(self, pk: str) -> None:
        '''

        Parameters
        ----------
        pk:

        Returns
        -------

        '''
        tenders_tag_df = pd.read_csv(self.tag_path)

        remain_list = [pk]
        for i in tenders_tag_df.columns:
            if 'key_' in i:
                remain_list.append(i)
        # TODO: adding weights -2022/4/1 Ray
        tenders_tag_df = tenders_tag_df[remain_list].melt(id_vars=pk)[[pk, 'value']].rename(
            columns={'value': 'tag'})
        tenders_tag_df = tenders_tag_df[tenders_tag_df['tag'].notna()]

        duplicated_df = tenders_tag_df.duplicated()
        assert not duplicated_df.empty, \
            f'This data set contains duplicated tags in tenders {duplicated_df[pk].unique()}'
        tenders_tag_df.to_csv(self.tag_map_path, index=0)

    def create_topic_mapping(self, pk) -> None:
        '''

        Parameters
        ----------
        pk

        Returns
        -------

        '''
        tenders_topic_df = pd.read_csv(self.topic_path)
        tenders_topic_df['values'] = tenders_topic_df.apply(self.__get_topic, axis=1).copy()
        tenders_topic_df = tenders_topic_df.set_index(pk)
        tenders_topic_df = tenders_topic_df[['values']].explode('values')
        tenders_topic_df = tenders_topic_df['values'].str.split(',',
                                                                expand=True).rename(columns={0: 'topic',
                                                                                             1: 'weight'}).reset_index()
        duplicated_df = tenders_topic_df.duplicated([pk, 'topic'])

        assert not duplicated_df.empty, \
            f'This data set contains duplicated tags in tenders {duplicated_df[pk].unique()}'
        tenders_topic_df.to_csv(self.topic_map_path, index=0)

    def create_all(self, pk: str):
        self.create_tag_mapping(pk)
        self.create_topic_mapping(pk)
