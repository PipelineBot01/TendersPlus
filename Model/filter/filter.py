import sys
import numpy as np
import pandas as pd

from conf.file_path import RESEARCHER_MOVEMENT
from researcher.matching.researcher_relation import ResearcherMatcher
from tenders.matching.tenders_relation import TendersMatcher
from utils.match_utils import normalize

WEIGHT_MAP = {1: 0.65}
sys.path.append('../../Model')


class Filter:
    def __init__(self, act_path=RESEARCHER_MOVEMENT):
        self.rm = ResearcherMatcher()
        self.tm = TendersMatcher()
        self.act_df = pd.read_csv(act_path)

    def __get_sim_researcher(self, r_id: str):
        result_df = self.rm.match_by_id(r_id)
        if result_df.empty:
            pass
        return result_df

    def __get_sim_tenders(self, t_id: str):
        result_df = self.tm.match(t_id)
        if result_df.empty:
            pass
        return result_df

    def tmp_measure(self, save_df: pd.DataFrame, act_tenders_df: pd.DataFrame) -> pd.DataFrame:
        '''

        Parameters
        ----------
        save_df
        act_tenders_df

        Returns
        -------

        '''
        save_df = save_df[~save_df['id'].isin(save_df['orig'])]
        re_weight_df = save_df.groupby(['id', 'orig']).agg({'weight': 'min'}).reset_index()
        merge_df = re_weight_df.merge(act_tenders_df, left_on='orig', right_on='t_id')
        del act_tenders_df, save_df

        merge_df['weight'] = merge_df['weight_x'] + 1.2 * merge_df['weight_y'] * (1 - merge_df['act_type'])
        re_weight_df = merge_df.groupby(['id']).agg({'weight': 'min'}).reset_index()
        re_cnt_df = merge_df.groupby('id')['orig'].count().reset_index().rename(columns={'orig': 'cnt'})
        merge_df = re_weight_df.merge(re_cnt_df, on='id')
        del re_cnt_df, re_weight_df

        merge_df = normalize(merge_df, 'cnt', 'max_min')
        merge_df['weight'] = merge_df['weight'] * (1 - np.tanh(merge_df['cnt']))

        return merge_df[['id', 'weight']]

    def match(self, r_id: str, func=tmp_measure) -> pd.DataFrame:
        '''

        Parameters
        ----------
        r_id
        func

        Returns
        -------

        '''
        sim_re_df = self.__get_sim_researcher(r_id)
        remain_movement = self.act_df.merge(sim_re_df, left_on='r_id', right_on='Staff ID')
        del sim_re_df

        remain_movement['act_type'] = remain_movement['act_type'].map(lambda x: WEIGHT_MAP[x])
        act_tenders_df = remain_movement.groupby('t_id').agg({'act_type': 'sum', 'weight': 'min'}).reset_index()
        act_tenders_df = normalize(act_tenders_df, 'weight', 'scaled_max_min')
        del remain_movement

        sim_tenders_df = pd.DataFrame()
        for tmp_id in act_tenders_df['t_id'].unique():
            tmp_df = self.__get_sim_tenders(tmp_id)
            tmp_df['orig'] = tmp_id
            tmp_df = normalize(tmp_df, 'weight', 'scaled_max_min')
            sim_tenders_df = sim_tenders_df.append(tmp_df)

        result_df = func(self, sim_tenders_df, act_tenders_df)
        return result_df.sort_values('weight')[:10].append(result_df.sort_values('weight')[-10:].sample(3))


if __name__ == '__main__':
    # pd.DataFrame({'r_id': ['Canberra61587c82d7b0c43ebd755358',
    #                        'Canberra61585b5dd7b0c43ebd7551eb',
    #                        'Canberra615861add7b0c43ebd755246',
    #                        'Canberra61587702d7b0c43ebd755322'],
    #               'time': [datetime.datetime.now(),
    #                        datetime.datetime.now(),
    #                        datetime.datetime.now(),
    #                        datetime.datetime.now()],
    #               't_id': ['Grants623afba2b34a6bd48ae4bd42',
    #                        'Grants623afbf6b34a6bd48ae4bd63',
    #                        'Grants623afc09b34a6bd48ae4bd6a',
    #                        'Grants623afc0fb34a6bd48ae4bd6c'],
    #               'act_type': [1, 1, 1, 1]}).to_csv('test.csv', index=0)
    filter = Filter()
    print(filter.match('Canberra61585cffd7b0c43ebd755201'))
