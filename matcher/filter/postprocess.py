import datetime

import pandas as pd

from conf.file_path import RESEARCHER_ACTION_PATH
from tenders.matching.tenders_relation import TendersMatcher

NOW_DATE = datetime.datetime.now()
SELF_ACT_LIST = [0, 1, 2]
DISLIKE_TYPE = 3


class PostProcess:
    def __init__(self, action_path=RESEARCHER_ACTION_PATH):
        self.action_df = pd.read_csv(action_path)
        self.action_df['action_date'] = pd.to_datetime(self.action_df['action_date'])

    def diff_month(self, date):
        return (NOW_DATE.year - date.year) * 12 + NOW_DATE.month - date.month

    def __get_hot_grants(self):
        tmp_df = self.action_df.copy()
        tmp_df['date'] = tmp_df['action_date'].dt.normalize()
        tmp_df = tmp_df.drop_duplicates(['id', 'type', 'go_id', 'date'])

        tmp_df.loc[datetime.datetime.now() - tmp_df['action_date'] < datetime.timedelta(days=7), '1_week'] = 1
        tmp_df['1_week'] = tmp_df['1_week'].fillna(0)
        tmp_df['1_month'] = tmp_df['action_date'].map(lambda x: self.diff_month(x))
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

    def __remove_dislike(self, user_id, input_df):
        dislike_df = input_df[(input_df['id'] == user_id) & (input_df['type'] == 5)]
        if not dislike_df.empty:
            input_df = input_df[~input_df['go_id'].isin(dislike_df['go_id'].unique())]
        return input_df

    def __decline_rmv_fav(self, user_id, input_df):
        remove_fav_df = input_df[(input_df['id'] == user_id) & (input_df['type'] == 3)]
        tm = TendersMatcher(tag_map_path='../tenders/assets/tenders_tag.csv',
                            topic_path='../tenders/assets/tenders_topic.csv',
                            info_path='../tenders/assets/clean_trains_info.csv')
        save_df = pd.DataFrame()
        for goid in remove_fav_df['go_id'].unique():
            save_df = save_df.append(tm.match(goid))
        

    def run(self, user_id, input_df):
        # remove dislike tenders
        self.__remove_dislike()
        self.__get_hot_grants()
