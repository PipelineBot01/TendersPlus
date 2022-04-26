import os
from typing import Dict
import numpy as np
import pandas as pd
from conf.file_path import RESEARCHER_ACTION_PATH, TENDERS_INFO_PATH, TENDERS_RELATION_MAP_PATH
from researcher.matching.researcher_relation import ResearcherMatcher
from tenders.matching.tenders_relation import TendersMatcher
from typing import List
from utils.match_utils import normalize

WEIGHT_MAP = {0: 0.1, 1: 0.25, 2: 0.45, 4: 0.75}


class Filter:
    def __init__(self, act_path=RESEARCHER_ACTION_PATH,
                 tenders_info_path=TENDERS_INFO_PATH,
                 tenders_relation_path = TENDERS_RELATION_MAP_PATH):
        self.__rm = ResearcherMatcher()
        self.__tm = TendersMatcher()
        self.__act_path = act_path
        self.__tenders_info_path = tenders_info_path
        self.__tenders_relation_path = tenders_relation_path

        self.__act_df = pd.read_csv(act_path)
        self.__tenders_info_df = pd.read_csv(tenders_info_path)
        self.__tenders_relation_df = pd.read_csv(tenders_relation_path)

    def tmp_measure(self, save_df: pd.DataFrame, act_tenders_df: pd.DataFrame) -> pd.DataFrame:
        '''

        Parameters
        ----------
        save_df
        act_tenders_df

        Returns
        -------

        '''
        save_df = save_df[~save_df['id'].isin(save_df['orig_id'])]
        re_weight_df = save_df.groupby(['id', 'orig_id']).agg({'weight': 'min'}).reset_index()
        merge_df = re_weight_df.merge(act_tenders_df, left_on='orig_id', right_on='t_id')
        del act_tenders_df, save_df

        merge_df['weight'] = (merge_df['weight_x'] + 1.2 * merge_df['weight_y']) * (1 - merge_df['type'])
        re_weight_df = merge_df.groupby(['id']).agg({'weight': 'min'}).reset_index()
        re_cnt_df = merge_df.groupby('id')['orig_id'].count().reset_index().rename(columns={'orig_id': 'cnt'})
        merge_df = re_weight_df.merge(re_cnt_df, on='id')
        del re_cnt_df, re_weight_df

        # merge_df = normalize(merge_df, 'cnt', 'max_min')
        # merge_df['weight'] = merge_df['weight'] * (1 - np.tanh(merge_df['cnt']))

        return merge_df[['id', 'weight']]

    def __reformat_result(self, input_df):
        merge_df = input_df.merge(self.__tenders_info_df, on='id')
        merge_df = merge_df[merge_df['go_id'].notna()]
        return merge_df['go_id'].to_list()

    def update_data(self):
        self.__rm = ResearcherMatcher()
        self.__tm = TendersMatcher()
        self.__act_df = pd.read_csv(self.__act_path)
        self.__tenders_info_df = pd.read_csv(self.__tenders_info_path)
        self.__tenders_relation_df = pd.read_csv(self.__tenders_relation_path)

    def match(self, profile_dict: Dict, func=tmp_measure) -> List[str]:
        '''

        Parameters
        ----------
        profile_dict
        func

        Returns
        -------

        '''
        if 'id' not in profile_dict.keys():
            profile_dict['id'] = ''

        if profile_dict['id'] != '':
            profile_dict['id'] = 'Reg_' + profile_dict['id']
        sim_re_df = self.__rm.match_by_profile(profile_dict, get_dict=False, remove_cur_id=False)
        remain_movement = self.__act_df.merge(sim_re_df, on='id')

        if remain_movement.empty:
            print(f'{profile_dict} with no similar data')
            # TODO: only for testing -Ray 2022/4/20
            profile_dict['divisions'] = '/'.join(i for i in profile_dict['divisions'])
            profile_dict['tags'] = '/'.join(i for i in profile_dict['tags'])
            if os.path.exists('missing_record.csv'):
                tmp_df = pd.read_csv('missing_record.csv')
                tmp_df.append(profile_dict, ignore_index=True).to_csv('missing_record.csv', index=0)
            else:
                pd.DataFrame(profile_dict, index=[0]).to_csv('missing_record.csv', index=0)
            return pd.DataFrame()
        del sim_re_df

        remain_movement = remain_movement[remain_movement['type'].isin(WEIGHT_MAP.keys())]
        remain_movement['type'] = remain_movement['type'].map(lambda x: WEIGHT_MAP[x])
        remain_movement.rename(columns={'id': 'r_id'}, inplace=True)
        remain_movement = remain_movement.merge(self.__tenders_info_df[['id', 'go_id']], on='go_id')
        remain_movement.rename(columns={'id': 't_id'}, inplace=True)

        tmp_df = remain_movement[remain_movement['weight'].notna()]

        if not tmp_df.empty:
            remain_movement.loc[remain_movement['r_id'] == profile_dict['id'], 'weight'] = np.mean(
                remain_movement[remain_movement['weight'].notna()]['weight'])
        else:
            remain_movement.loc[remain_movement['r_id'] == profile_dict['id'], 'weight'] = 1 / len(remain_movement)
        act_tenders_df = remain_movement.groupby('t_id').agg({'type': 'max', 'weight': 'min'}).reset_index()
        act_tenders_df = normalize(act_tenders_df, 'weight', 'scaled_max_min')
        del remain_movement

        sim_tenders_df = pd.DataFrame()
        for tmp_id in act_tenders_df['t_id'].unique():
            tmp_df = self.__tenders_relation_df[self.__tenders_relation_df['orig_id'] == tmp_id]
            tmp_df = normalize(tmp_df, 'weight', 'scaled_max_min')
            sim_tenders_df = sim_tenders_df.append(tmp_df)
        result_df = func(self, sim_tenders_df, act_tenders_df)

        return self.__reformat_result(result_df.sort_values('weight'))

