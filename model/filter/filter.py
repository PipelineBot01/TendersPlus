import sys
import numpy as np
import pandas as pd
import datetime
from conf.file_path import RESEARCHER_MOVEMENT
from researcher.matching.researcher_relation import ResearcherMatcher
from tenders.matching.tenders_relation import TendersMatcher
from utils.match_utils import normalize

WEIGHT_MAP = {1: 0.55, 2: 0.75}
sys.path.append('..')


class Filter:
    def __init__(self, act_path=RESEARCHER_MOVEMENT):
        self.__rm = ResearcherMatcher()
        self.__tm = TendersMatcher()
        self.__act_df = pd.read_csv(act_path)

    def __get_sim_researcher(self, r_id: str):
        result_df = self.__rm.match_by_id(r_id)
        if result_df.empty:
            pass
        return result_df

    def __get_sim_tenders(self, t_id: str):
        result_df = self.__tm.match(t_id)
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

        merge_df['weight'] = (merge_df['weight_x'] + 1.2 * merge_df['weight_y']) * (1 - merge_df['act_type'])
        re_weight_df = merge_df.groupby(['id']).agg({'weight': 'min'}).reset_index()
        re_cnt_df = merge_df.groupby('id')['orig'].count().reset_index().rename(columns={'orig': 'cnt'})
        merge_df = re_weight_df.merge(re_cnt_df, on='id')
        del re_cnt_df, re_weight_df

        # merge_df = normalize(merge_df, 'cnt', 'max_min')
        # merge_df['weight'] = merge_df['weight'] * (1 - np.tanh(merge_df['cnt']))

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
        remain_movement = self.__act_df.merge(sim_re_df, left_on='r_id', right_on='Staff ID')
        del sim_re_df

        remain_movement['act_type'] = remain_movement['act_type'].map(lambda x: WEIGHT_MAP[x])
        act_tenders_df = remain_movement.groupby('t_id').agg({'act_type': 'max', 'weight': 'min'}).reset_index()
        act_tenders_df = normalize(act_tenders_df, 'weight', 'scaled_max_min')
        del remain_movement

        sim_tenders_df = pd.DataFrame()
        for tmp_id in act_tenders_df['t_id'].unique():
            tmp_df = self.__get_sim_tenders(tmp_id)
            tmp_df['orig'] = tmp_id
            tmp_df = normalize(tmp_df, 'weight', 'scaled_max_min')
            sim_tenders_df = sim_tenders_df.append(tmp_df)

        result_df = func(self, sim_tenders_df, act_tenders_df)
        return result_df.sort_values('weight')
        # return result_df.sort_values('weight')[:10].append(result_df.sort_values('weight')[-10:].sample(3))


if __name__ == '__main__':
    # Research Institute for Sport & Exercise  -visit-  Arthritis Information, Education and Support [high relation]
    # Sport & Exercise Science  -visit-  National Disability Insurance Agency (NDIA)  [relation]
    # Physiotherapy  -visit-  Mental Health in Mulitcultural Australia  [low relation]
    # Sport & Exercise Science  -visit-  Department of Health (Indigenous Remote Service Delivery Traineeship NT)  [noise]
    # Canberra School of Politics, Economics and Society  -visit-  National Health and Medical Research Council (NHMRC) [noise]
    # Business, Government & Law Office  -visit-  Regional Jobs and Investment Packages - Tropical North Queensland region [noise]
    pd.DataFrame({'r_id': ['Canberra61587c82d7b0c43ebd755358',
                           'Canberra615861add7b0c43ebd755246',
                           'Canberra615871d1d7b0c43ebd7552f7',
                           'Canberra61585a56d7b0c43ebd7551dd',
                           'Canberra61585a81d7b0c43ebd7551e1',
                           'Canberra61585c9cd7b0c43ebd7551fa'],
                  'time': [datetime.datetime.now(),
                           datetime.datetime.now(),
                           datetime.datetime.now(),
                           datetime.datetime.now(),
                           datetime.datetime.now(),
                           datetime.datetime.now()],
                  't_id': ['Grants623b012fb34a6bd48ae4bf53',
                           'Grants623afc09b34a6bd48ae4bd6a',
                           'Grants623afbf6b34a6bd48ae4bd63',
                           'Grants623afc0fb34a6bd48ae4bd6c',
                           'Grants623afc13b34a6bd48ae4bd6d',
                           'Grants623afbb2b34a6bd48ae4bd49'],
                  'act_type': [2, 1, 1, 1, 1, 1]}).to_csv('assets/test.csv', index=0)
    filter = Filter()
    print(filter.match('Canberra61585cffd7b0c43ebd755201')) #Health Office
