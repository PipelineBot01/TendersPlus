import os
import re
from typing import List, Dict

import numpy as np
import pandas as pd

TENDERS_TAG_PATH = '../assets/tenders_keyword.csv'

id_reg_rule = r'\'(.*?)\''


class TendersRelation:
    def __init__(self, orig_tenders_df: pd.DataFrame):
        self.__key_cols = ['_id', 'key_0', 'key_1', 'key_2', 'key_3', 'key_4']

        self.__mapping_df = None

        #  Generating a new mapping file if no file under this directory.
        if not os.path.exists(TENDERS_TAG_MAP_PATH):
            self.__generate_mapping_file(TENDERS_TAG_MAP_PATH)

        self.__mapping_df = pd.read_csv(TENDERS_TAG_MAP_PATH)

        self.__orig_df = orig_tenders_df

        self.__tag_df = self.__orig_df[self.__key_cols]

        # TODO: Add delta data checking method and complete mapping table function later - 2022.3.37 Ray



    def direct_similarity(self, tenders_id: str, tags: List[str]) -> Dict[int, str]:
        '''

        Parameters
        ----------
        tenders_id: str, the id for tender that will be matched.
        tags: tag for the tender.

        This function is just a trail for matching.

        Returns
        -------
        Dict[int, str], matching result, with key as matching level and value as matched tenders.
        '''

        candidate_list = []
        for tag in tags:
            candidate_list.append(re.findall(id_reg_rule,
                                             self.__mapping_df[self.__mapping_df['tag'] == tag]['_ids'].values[0]))

        if len(candidate_list) == 0:
            return {}
        key_0_set = set(candidate_list[0])
        key_0_set.remove(tenders_id)
        cnt_dict = {0: key_0_set}
        for idx in range(1, len(candidate_list)):
            cnt_dict[idx] = cnt_dict[idx - 1].intersection(set(candidate_list[idx]))

        # TODO: Temporary return dict, need to unify the return type when we expand new methods - 2022.3.37 Ray
        return cnt_dict

    def get_similar_tenders(self, tenders_id: str, measure_func=direct_similarity) -> pd.DataFrame:
        '''

        Parameters
        ----------
        tenders_id: str, the id for tender that will be matched.
        measure_func: function, the measure function

        Returns
        -------
        tmp, currently return a dataframe with the matching result.

        '''
        tenders_df = self.__orig_df[self.__orig_df['_id'] == tenders_id]
        filter_df = tenders_df[self.__key_cols].dropna(axis=1)
        print('---', filter_df)
        tag_list = filter_df.values.tolist()[0]
        # print('---', tag_list)
        matching_dict = measure_func(self, tag_list[0], tag_list[1:])

        # TODO: Temporary code - 2022.3.37 Ray
        #############################################################################################################
        test_cols = {'Title': 'Ori_Title',
                     'Category': 'Ori_Category',
                     'Description': 'Ori_Description'}

        check_df = tenders_df[['_id'] + list(test_cols.keys())].rename(columns=test_cols)
        check_df = check_df.reset_index()
        check_df['index'] = 0

        result_cols = {'Title': 'Res_Title',
                       'Category': 'Res_Category',
                       'Description': 'Res_Description'}

        matching_dict.pop(0)
        tmp_list = []
        for k, v in matching_dict.items():
            for tenders_id in v:
                tmp_df = self.__orig_df[self.__orig_df['_id'] == tenders_id].rename(columns=result_cols)
                tmp_df['level'] = k
                tmp_list.append(tmp_df)
        if len(tmp_list) > 0:
            result_df = pd.concat(tmp_list, ignore_index=True)[['level'] + list(result_cols.values())].reset_index()
        else:
            result_df = pd.DataFrame({'Res_Title': [np.nan], 'Res_Category': [np.nan], 'Res_Description': [np.nan]})
        result_df['index'] = 0

        merge_df = check_df.merge(result_df, on='index', how='right').drop('index', axis=1)
        del check_df, result_df
        #############################################################################################################

        return merge_df


if __name__ == '__main__':
    tenders_tag_df = pd.read_csv(TENDERS_TAG_PATH)
    tr = TendersRelation(tenders_tag_df)
    test_list = []
    for i in range(300):
        test_df = tenders_tag_df.sample(1)
        print(test_df)
        result_df = tr.get_similar_tenders(test_df['_id'].values[0])
        test_list.append(result_df)
    pd.concat(test_list, ignore_index=True).to_csv('tender_matching.csv', index=0, encoding='utf-8_sig')

# TODO: 6162aa1fe1b7f5c73e6fea50, 6162aa1fe1b7f5c73e6fe68f, 6162aa1fe1b7f5c73e6fea50
