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
        self.__action_df = pd.read_csv(action_path)
        self.__info_df = pd.read_csv(info_path)
        self.__action_df['action_date'] = pd.to_datetime(self.__action_df['action_date'])

    def __diff_month(self, date):
        return (NOW_DATE.year - date.year) * 12 + NOW_DATE.month - date.month

    def __reformat_user_action(self):
        self.__action_df.loc[(self.__action_df['type'] == 2) | (self.__action_df['type'] == 3), 'save'] = 1
        self.__action_df.loc[(self.__action_df['type'] == 4) | (self.__action_df['type'] == 5), 'like'] = 1

        action_df = self.__action_df.sort_values('action_date', ascending=False)
        save_df = action_df[action_df['save'] == 1].drop_duplicates(['id', 'type', 'go_id'], keep='first')
        like_df = action_df[action_df['like'] == 1].drop_duplicates(['id', 'type', 'go_id'], keep='first')

        remain_df = self.__action_df[self.__action_df.isna().any(axis=1)]
        action_df = remain_df.append(save_df).append(like_df).merge(self.__info_df, on='go_id')
        del self.__info_df
        return action_df

    def __remove_dislike(self, user_id, input_df):
        dislike_df = self.__action_df[(self.__action_df['id'] == user_id) & (self.__action_df['type'] == 5)]
        if not dislike_df.empty:
            input_df = input_df[~input_df['go_id'].isin(dislike_df['go_id'].unique())]
        return input_df

    def __reformat_fav(self, user_id, input_df):
        fav_df = self.__action_df[(self.__action_df['id'] == user_id) & (self.__action_df['type'] == 2)]
        if not fav_df.empty:
            tmp_df = input_df[input_df['go_id'].isin(fav_df['go_id'].unique())].sort_values('weight')
            input_df = tmp_df.append(input_df[~input_df['go_id'].isin(fav_df['go_id'].unique())])
        return input_df

    def __reformat_rmv_fav(self, user_id, input_df):
        remove_fav_df = self.__action_df[(self.__action_df['id'] == user_id) & (self.__action_df['type'] == 3)]
        tm = TendersMatcher(tag_map_path='../tenders/assets/tenders_tag.csv',
                            topic_path='../tenders/assets/tenders_topic.csv',
                            info_path='../tenders/assets/clean_trains_info.csv')

        rel_save_df = []
        tar_save_df = remove_fav_df['id'].unique().tolist()
        for t_id in remove_fav_df['id'].unique():
            rel_save_df = rel_save_df + tm.match(t_id)['id'].unique().tolist()

        cond_rel = input_df['go_id'].isin(rel_save_df)
        input_df.loc[cond_rel, 'weight'] = input_df[cond_rel]['weight']+sum(input_df['weight'])/3
        del cond_rel

        cond_tar = input_df['go_id'].isin(tar_save_df)
        input_df.loc[cond_tar, 'weight'] = input_df[cond_tar]['weight'] + sum(input_df['weight']) / 2
        return input_df.sort_values('weight')

    def get_hot_tenders(self):
        tmp_df = self.__action_df.copy()
        tmp_df['date'] = tmp_df['action_date'].dt.normalize()
        tmp_df = tmp_df.drop_duplicates(['id', 'type', 'go_id', 'date'])

        tmp_df.loc[datetime.datetime.now() - tmp_df['action_date'] < datetime.timedelta(days=7), '1_week'] = 1
        tmp_df['1_week'] = tmp_df['1_week'].fillna(0)
        tmp_df['1_month'] = tmp_df['action_date'].map(lambda x: self.__diff_month(x))
        tmp_df['3_month'] = tmp_df['1_month']
        tmp_df.loc[tmp_df['1_month'] < 2, '1_month'] = 1
        tmp_df['1_month'] = tmp_df['1_month'].fillna(0)
        tmp_df.loc[tmp_df['3_month'] < 4, '3_month'] = 1
        tmp_df['3_month'] = tmp_df['3_month'].fillna(0)

        save_list = []
        for window in ['1_week', '1_month', '3_month']:
            tmp_hot_df = tmp_df[(tmp_df['type'].isin(SELF_ACT_LIST)) & (tmp_df[window])].groupby('go_id')[
                'id'].count().reset_index().rename(columns={'id': 'cnt'}
                                                   ).sort_values('cnt', ascending=False).reset_index(drop=True
                                                                                                     ).reset_index()
            save_list.append(tmp_hot_df)
        return save_list


    def __reformat_location(self):
        pass

    def __reformat_others(self):
        pass



    def run(self, user_id, input_df):

        self.__action_df = self.__reformat_user_action()

        # remove dislike tenders
        self.__remove_dislike(user_id, input_df)

        # reformat favourite tenders
        self.__reformat_fav(user_id, input_df)

        # reformat removed favourite tenders
        self.__reformat_rmv_fav(user_id, input_df)
