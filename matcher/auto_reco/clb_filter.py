import os
import datetime
from typing import Dict
import numpy as np
import pandas as pd
from conf.file_path import RESEARCHER_ACTION_PATH, \
    TENDERS_INFO_PATH, TENDERS_RELATION_MAP_PATH, TENDERS_CATE_DIV_MAP_PATH
from researcher.matching.researcher_relation import ResearcherMatcher
from tenders.matching.tenders_relation import TendersMatcher
from typing import List
from utils.match_utils import normalize
from utils.match_utils import get_div_id_dict

WEIGHT_MAP = {0: 0.1, 1: 0.25, 2: 0.45, 4: 0.75}
SELF_ACT_LIST = [0, 1, 2]


class Filter:
    def __init__(self, act_path=RESEARCHER_ACTION_PATH,
                 tenders_info_path=TENDERS_INFO_PATH,
                 tenders_relation_path=TENDERS_RELATION_MAP_PATH,
                 cate_div_map_path=TENDERS_CATE_DIV_MAP_PATH):
        self.__rm = ResearcherMatcher()
        self.__tm = TendersMatcher()
        self.__act_path = act_path
        self.__tenders_info_path = tenders_info_path
        self.__tenders_relation_path = tenders_relation_path

        self.__act_df = pd.read_csv(act_path)
        self.__tenders_info_df = pd.read_csv(tenders_info_path)
        self.__tenders_relation_df = pd.read_csv(tenders_relation_path)
        self.__cate_div_map_df = pd.read_csv(cate_div_map_path)

    def tmp_measure(self, save_df: pd.DataFrame, act_tenders_df: pd.DataFrame) -> pd.DataFrame:
        '''

        Parameters
        ----------
        save_df
        act_tenders_df

        Returns
        -------

        '''
        save_df = save_df[save_df['id'].isin(save_df['orig_id'])]
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

    def __add_division_penalty(self, input_df, division):
        melt_df = input_df[['go_id', 'category', 'sub_category']].melt(id_vars='go_id')[['go_id', 'value']]
        melt_df = melt_df.merge(self.__cate_div_map_df, left_on='value', right_on='category')
        melt_df.drop_duplicates(['go_id', 'division'], inplace=True)
        on_div_df = melt_df[melt_df['division'].isin(division)]
        out_div_df = melt_df[~melt_df['go_id'].isin(on_div_df['go_id'])]

        out_df = input_df[input_df['go_id'].isin(out_div_df['go_id'])][['go_id', 'weight']]
        on_df = input_df[input_df['go_id'].isin(on_div_df['go_id'])][['go_id', 'weight']]
        out_df['weight'] = out_df['weight'] * 5
        return on_df, out_df

    def __reformat_result(self, input_df, cold_start_df, division):
        merge_df = input_df.merge(self.__tenders_info_df, on='id')
        merge_df = merge_df[merge_df['go_id'].notna()]
        on_df, out_df = self.__add_division_penalty(merge_df, division)
        if on_df.empty:
            on_df = cold_start_df
            on_df['weight'] = np.mean(out_df[:8]['weight'])/on_df['cnt']
        return on_df[['go_id', 'weight']].append(out_df).sort_values('weight').drop_duplicates('go_id', keep='first')

    def __diff_month(self, date, cur_date):
        return (cur_date.year - date.year) * 12 + cur_date.month - date.month

    def get_hot_tenders(self):
        if self.__act_df.empty:
            return []
        tmp_df = self.__act_df.copy()
        tmp_df['date'] = pd.to_datetime(tmp_df['action_date'])
        tmp_df = tmp_df.drop_duplicates(['id', 'type', 'go_id', 'date'])
        cur_date = datetime.datetime.now()
        tmp_df['1_month'] = tmp_df['date'].map(lambda x: self.__diff_month(x, cur_date))
        tmp_df.loc[tmp_df['1_month'] < 2, '1_month'] = 1
        tmp_df['1_month'] = tmp_df['1_month'].fillna(0)

        hot_df = tmp_df[(tmp_df['type'].isin(SELF_ACT_LIST)) & (tmp_df['1_month'])
                        ].groupby('go_id')['id'].count().reset_index().rename(columns={'id': 'cnt'}).sort_values(
            'cnt', ascending=False).reset_index(drop=True).reset_index()
        return hot_df['go_id'].tolist()

    def update(self):
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

        filter_info_df = self.__tenders_info_df[self.__tenders_info_df['go_id'].notna()]
        melt_df = filter_info_df[['go_id', 'category', 'sub_category']].melt(id_vars='go_id')[['go_id', 'value']]
        melt_df = melt_df.merge(self.__cate_div_map_df, left_on='value', right_on='category')
        melt_df.drop_duplicates(['go_id', 'division'], inplace=True)
        div_dict = get_div_id_dict()
        melt_df['division'] = melt_df['division'].map(lambda x: div_dict[x])
        melt_df = melt_df[melt_df['division'].isin(profile_dict['divisions'])]
        cold_start_df = melt_df.groupby('go_id'
                                        )['division'].count().reset_index().rename(columns={'division': 'cnt'}
                                                                                   ).sort_values('cnt', ascending=False)
        del sim_re_df

        if remain_movement.empty:
            print(f'{profile_dict} with no similar data')
            return cold_start_df

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

        return self.__reformat_result(result_df.sort_values('weight'), cold_start_df, profile_dict['divisions'])

