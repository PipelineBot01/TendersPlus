import pandas as pd
from typing import Dict
from conf.file_path import TENDERS_EMAIL_PATH, TENDERS_INFO_PATH, RESEARCHER_ACTION_PATH, \
    TENDERS_CATE_DIV_MAP_PATH, RESEARCHER_DIVISION_MAP_PATH
from tenders.matching.tenders_relation import TendersMatcher

ACTION_LIST = [0, 1, 2, 4]


def get_email_content() -> Dict:
    tenders_email_df = pd.read_csv(TENDERS_EMAIL_PATH)
    tenders_info_df = pd.read_csv(TENDERS_INFO_PATH)
    researcher_action_df = pd.read_csv(RESEARCHER_ACTION_PATH)
    cate_div_map_df = pd.read_csv(TENDERS_CATE_DIV_MAP_PATH)
    researcher_div_df = pd.read_csv(RESEARCHER_DIVISION_MAP_PATH)

    merge_df = tenders_info_df.merge(tenders_email_df, on='go_id')
    cate_df = merge_df[['id', 'category', 'sub_category']].melt('id').dropna()[['id', 'value']]
    cate_df = cate_df.dropna().merge(cate_div_map_df, left_on='value', right_on='category')[['division']]
    del tenders_email_df
    action_df = researcher_action_df[researcher_action_df['type'].isin(ACTION_LIST)]
    del researcher_action_df
    remain_df = action_df[['go_id',
                           'id']].merge(tenders_info_df[['go_id',
                                                         'id']].rename(columns={'id': 't_id'}
                                                                       ), on='go_id').drop_duplicates(['id', 't_id'])
    del tenders_info_df

    tm = TendersMatcher()
    save_dict = {}
    for t_id in merge_df['id']:
        go_id = merge_df[merge_df['id'] == t_id]['go_id'].values[0]
        tmp_df = tm.match(t_id, 20).rename(columns={'id': 't_id'})
        result_df = tmp_df.merge(remain_df, on='t_id')[['id']]

        tmp_df = cate_df.merge(researcher_div_df, on='division').drop_duplicates(['id'])[['id']]
        tmp_df = tmp_df[tmp_df['id'].str.startswith('Reg_')]
        final_df = result_df.append(tmp_df).drop_duplicates(['id'])
        for r_id in final_df['id']:
            save_dict[r_id] = [go_id] if r_id not in save_dict.keys() else save_dict[r_id].append(go_id)
    pd.DataFrame({'go_id': []}).to_csv(TENDERS_EMAIL_PATH, index=0)
    return save_dict
