import datetime

import pandas as pd

from conf.file_path import RESEARCHER_ACTION_PATH, TENDERS_INFO_PATH
from tenders.matching.tenders_relation import TendersMatcher

NOW_DATE = datetime.datetime.now()
SELF_ACT_LIST = [0, 1, 2]
DISLIKE_TYPE = 3


class PostProcess:
    def __init__(self, action_path=RESEARCHER_ACTION_PATH,
                 info_path=TENDERS_INFO_PATH):
        self.__action_path = action_path
        self.__info_path = info_path

        self.__action_df = pd.read_csv(action_path)
        self.__info_df = pd.read_csv(info_path)[['id', 'go_id']]
        if not self.__action_df.empty:
            self.__action_df['action_date'] = pd.to_datetime(self.__action_df['action_date'])
            self.__action_df = self.__reformat_user_action()

    def __diff_month(self, date):
        return (NOW_DATE.year - date.year) * 12 + NOW_DATE.month - date.month

    def update(self):
        self.__action_df = pd.read_csv(self.__action_path)
        self.__info_df = pd.read_csv(self.__info_path)
        if not self.__action_df.empty:
            self.__action_df['action_date'] = pd.to_datetime(self.__action_df['action_date'])
            self.__action_df = self.__reformat_user_action()

    def __reformat_user_action(self):
        tmp_df = self.__action_df.copy()
        tmp_df.loc[(tmp_df['type'] == 2) | (tmp_df['type'] == 3), 'save'] = 1
        tmp_df.loc[(tmp_df['type'] == 4) | (tmp_df['type'] == 5), 'like'] = 1

        action_df = tmp_df.sort_values('action_date', ascending=False)
        save_df = action_df[action_df['save'] == 1].drop_duplicates(['id', 'go_id'], keep='first')
        like_df = action_df[action_df['like'] == 1].drop_duplicates(['id', 'go_id'], keep='first')
        remain_df = tmp_df[(tmp_df['save'].isna()) & (tmp_df['like'].isna())]
        del tmp_df
        action_df = remain_df.append(save_df).append(like_df).rename(columns={'id': 'r_id'}
                                                                     ).merge(self.__info_df, on='go_id')
        return action_df

    def __remove_dislike(self, user_id, input_df):
        tmp_df = self.__action_df.copy()
        dislike_df = tmp_df[(tmp_df['r_id'] == user_id) & (tmp_df['type'] == 5)]
        del tmp_df
        if not dislike_df.empty:
            input_df = input_df[~input_df['go_id'].isin(dislike_df['go_id'].unique())]
        return input_df

    def __reformat_fav(self, user_id, input_df):
        fav_df = self.__action_df[(self.__action_df['r_id'] == user_id) & (self.__action_df['type'] == 2)].copy()
        if not fav_df.empty:
            input_df = fav_df.append(input_df[~input_df['go_id'].isin(fav_df['go_id'].unique())])
        return input_df

    def __reformat_rmv_fav(self, user_id, input_df):
        remove_fav_df = self.__action_df[(self.__action_df['r_id'] == user_id) & (self.__action_df['type'] == 3)].copy()
        tm = TendersMatcher()

        rel_save_df = []
        tar_save_df = remove_fav_df['id'].unique().tolist()
        for t_id in remove_fav_df['id'].unique():
            rel_save_df = rel_save_df + tm.match(t_id)['id'].unique().tolist()

        cond_rel = input_df['go_id'].isin(rel_save_df)
        input_df.loc[cond_rel, 'weight'] = input_df[cond_rel]['weight'] + sum(input_df['weight']) / 3
        del cond_rel

        cond_tar = input_df['go_id'].isin(tar_save_df)
        input_df.loc[cond_tar, 'weight'] = input_df[cond_tar]['weight'] + sum(input_df['weight']) / 2
        return input_df.sort_values('weight')
    
    def get_hot_tenders(self):
        if self.__action_df.empty:
            return []
        tmp_df = self.__action_df.copy()
        tmp_df['date'] = tmp_df['action_date'].dt.normalize()
        tmp_df = tmp_df.drop_duplicates(['r_id', 'type', 'go_id', 'date'])

        tmp_df['1_month'] = tmp_df['action_date'].map(lambda x: self.__diff_month(x))
        tmp_df.loc[tmp_df['1_month'] < 2, '1_month'] = 1
        tmp_df['1_month'] = tmp_df['1_month'].fillna(0)

        hot_df = tmp_df[(tmp_df['type'].isin(SELF_ACT_LIST)) & (tmp_df['1_month'])
                        ].groupby('go_id')['r_id'].count().reset_index().rename(columns={'r_id': 'cnt'}).sort_values(
            'cnt', ascending=False).reset_index(drop=True).reset_index()
        return hot_df['go_id'].tolist()

    def __reformat_location(self):
        pass

    def __reformat_others(self):
        pass

    def run(self, user_id, input_df):
        try:
            if user_id in self.__action_df['r_id'].unique():
                # remove dislike tenders
                input_df = self.__remove_dislike(user_id, input_df)
                # reformat favourite tenders
                input_df = self.__reformat_fav(user_id, input_df)

                # reformat removed favourite tenders
                input_df = self.__reformat_rmv_fav(user_id, input_df)
        except:
            print(self.__action_df.columns)
        return input_df['go_id'].tolist()
