import os
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd

from conf.file_path import TENDERS_INFO_PATH, TENDERS_TOPIC_MAP_PATH, TENDERS_TAG_MAP_PATH
from tenders.features.tenders_feat_creator import TendersFeatCreator
from utils.match_utils import normalize, weighted_avg


class TendersMatcher:
    def __init__(self, tag_map_path=TENDERS_TAG_MAP_PATH,
                 topic_path=TENDERS_TOPIC_MAP_PATH,
                 info_path=TENDERS_INFO_PATH, pk='id'):
        #  Generating required file if no file under this directory.

        tfc = TendersFeatCreator()
        if not os.path.exists(tag_map_path):
            tfc.create_tag_mapping(pk)
        if not os.path.exists(topic_path):
            tfc.create_topic_mapping(pk)

        self.pk = pk
        self.__info_df = pd.read_csv(info_path)
        self.__tag_df = pd.read_csv(tag_map_path)
        self.__topic_df = pd.read_csv(topic_path)

    def __prepare_dataset(self, tenders_id: str) -> Tuple[list, list]:
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
        candidate_df = ref_df[ref_df['tag'].isin(tar_df['tag'])]
        candidate_df = candidate_df.groupby(self.pk)['tag'].count().reset_index().rename(
            columns={'tag': 'weight'}).sort_values('weight', ascending=False)
        candidate_df = normalize(candidate_df, 'weight', 'max_min')
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
            tmp_df1['weight'] = tmp_df1['weight_y'] - 1.2 * tmp_df1['weight_x']
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
        topic_list, tag_list = self.__prepare_dataset(tenders_id)
        candidate_df = measure_func(self, topic_list, tag_list)

        # handle no enough matching result
        if len(candidate_df) < match_num:
            tmp_info_df = self.__info_df[self.__info_df[self.pk] == tenders_id]
            others_df = self.__info_df[self.__info_df[self.pk] != tenders_id]
            tmp_df = others_df[others_df['category'].isin(tmp_info_df['category'])].sample(frac=1)[[self.pk]]
            tmp2_df = others_df[others_df['agency'].isin(tmp_info_df['agency'])].sample(frac=1)[[self.pk]]
            candidate_df = candidate_df.append(tmp_df).append(tmp2_df)
            candidate_df['weight'] = candidate_df['weight'].fillna(1/len(candidate_df))
        return candidate_df[:min(match_num, len(candidate_df))]
