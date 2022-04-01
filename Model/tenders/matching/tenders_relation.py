import os
from typing import List, Dict

import numpy as np
import pandas as pd

from conf.file_path import TENDERS_INFO_PATH, TENDERS_TAG_PATH, \
    TENDERS_TOPIC_PATH, TENDERS_TAG_MAP_PATH, TENDERS_TOPIC_MAP_PATH, TENDERS_MATCHING_OUTPUT
from relation_interface.Relation import Relation
from tenders.features.tenders_feat_creator import TendersFeatCreator
from utils.match_utils import normalize, weighted_avg


class TendersMatcher(Relation):
    def __init__(self, pk: str):
        #  Generating required file if no file under this directory.

        tfc = TendersFeatCreator()
        if not os.path.exists(TENDERS_TAG_MAP_PATH):
            tfc.create_tag_mapping(pk)
        if not os.path.exists(TENDERS_TOPIC_PATH):
            tfc.create_topic_mapping(pk)

        self.pk = pk
        self.__info_df = pd.read_csv(TENDERS_INFO_PATH)
        self.__tag_df = pd.read_csv(TENDERS_TAG_MAP_PATH)
        self.__topic_df = pd.read_csv(TENDERS_TOPIC_MAP_PATH)

    def prepare_dataset(self, tenders_id: str) -> tuple[list, list]:
        '''

        Parameters
        ----------
        tenders_id

        Returns
        -------

        '''
        assert tenders_id in self.__info_df[self.pk].unique(), f'No such researcher {self.pk}: {tenders_id}'

        tar_tag_df = self.__tag_df[self.__tag_df[self.pk] == tenders_id]
        ref_tag_df = self.__tag_df[self.__tag_df[self.pk] != tenders_id]
        tar_topic_df = self.__topic_df[self.__topic_df[self.pk] == tenders_id]
        ref_topic_df = self.__topic_df[self.__topic_df[self.pk] != tenders_id]

        return [tar_topic_df, ref_topic_df], [tar_tag_df, ref_tag_df]

    def __dir_tag_sim(self, tar_df: pd.DataFrame, ref_df: pd.DataFrame) -> Dict[int, str]:
        '''

        Parameters
        ----------
        tar_df
        ref_df

        Returns
        -------

        '''
        candidate_df = ref_df[ref_df['Tag'].isin(tar_df['Tag'])]
        candidate_df = candidate_df.groupby(self.pk)['Tag'].count().reset_index().rename(
            columns={'Tag': 'weight'}).sort_values('weight', ascending=False)
        candidate_df = normalize(candidate_df, 'weight', 'max-min')
        return candidate_df

    def __weight_topic_sim(self, tar_df: pd.DataFrame, ref_df: pd.DataFrame) -> pd.DataFrame:
        '''

        Parameters
        ----------
        tar_df
        ref_df

        Returns
        -------

        '''
        merge_df = ref_df.merge(tar_df, on='topic', suffixes=('', '_y'))
        merge_df['weight'] = abs(merge_df['weight'] - merge_df['weight_y'])
        merge_df = weighted_avg(merge_df, self.pk, self.pk + '_y')
        if merge_df.empty:
            return merge_df
        return merge_df[[self.pk, 'weight']].drop_duplicates()

    def __combined_measure(self, topic_list: List[pd.DataFrame], tag_list: List[pd.DataFrame]) -> pd.DataFrame:
        '''

        Parameters
        ----------
        topic_list
        tag_list

        Returns
        -------

        '''
        tmp_df1 = self.__dir_tag_sim(*tag_list)
        tmp_df2 = self.__weight_topic_sim(*topic_list)

        if not tmp_df1[tmp_df1['weight'].notna()].empty:
            tmp_df1 = tmp_df1.merge(tmp_df2, on=self.pk, how='outer')
            tmp_df1['weight_x'].fillna(np.mean(tmp_df1['weight_x']))
            tmp_df1['weight_y'].fillna(np.mean(tmp_df1['weight_y']))
            tmp_df1['weight'] = tmp_df1['weight_y'] - tmp_df1['weight_x']
        del tmp_df2
        return tmp_df1.sort_values('weight')[[self.pk, 'weight']]

    def match(self, tenders_id: str, match_num=10, measure_func=__combined_measure) -> pd.DataFrame:
        '''

        Parameters
        ----------
        tenders_id
        match_num
        measure_func

        Returns
        -------

        '''
        topic_list, tag_list = self.prepare_dataset(tenders_id)
        candidate_df = measure_func(self, topic_list, tag_list)

        # handle no enough matching result
        if len(candidate_df) < match_num:
            tmp_info_df = self.__info_df[self.__info_df[self.pk] == tenders_id]
            candidate_df = candidate_df.append(self.__info_df[self.__info_df['category'] == tmp_info_df['category']])
        return candidate_df[:match_num]


if __name__ == '__main__':
    tenders_tag_df = pd.read_csv(TENDERS_TAG_PATH)
    tr = TendersMatcher('_id')
    test_list = []
    # print('start')
    # result_df = tr.match('6162aa1fe1b7f5c73e6fe6bf')
    # print(result_df)
    for i in range(20):
        test_df = tenders_tag_df.sample(1)
        print(test_df['_id'])
        result_df = tr.match(test_df['_id'].values[0])
        result_df.loc[:, 'orig_id'] = test_df['_id'].values[0]
        test_list.append(result_df)
    pd.concat(test_list, ignore_index=True).to_csv(TENDERS_MATCHING_OUTPUT, index=0, encoding='utf-8_sig')
