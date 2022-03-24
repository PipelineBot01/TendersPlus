from typing import List, Dict, Optional

import numpy as np
import pandas as pd

from conf.division import RESEARCH_FIELDS
from conf.file_path import RESEARCHER_TAG_MAP_PATH, RESEARCHER_DIVISION_MAP_PATH, \
    RESEARCHER_TAG_CATE_MAP_PATH, RESEARCHER_INFO_PATH
from relation_interface.Relation import Relation
from utils.match_utils import normalize, weighted_avg

MAP_DF = pd.read_pickle(RESEARCHER_TAG_CATE_MAP_PATH)
INFO_DF = pd.read_pickle(RESEARCHER_INFO_PATH)


class ResearcherMatcher(Relation):
    def __init__(self, re_div_path=RESEARCHER_DIVISION_MAP_PATH, re_tag_path=RESEARCHER_TAG_MAP_PATH, pk='Staff ID'):
        self.re_div_df = pd.read_pickle(re_div_path)
        self.re_tag_df = pd.read_pickle(re_tag_path)
        self.pk = pk

        assert not self.re_div_df.empty, 'Cannot generate matcher due to empty file!'
        assert not (self.re_div_df.duplicated(pk).empty and self.re_tag_df.duplicated(pk).empty), \
            f'{pk} cannot be set as primary key!'

    def __weighted_div_sim(self, tar_df: pd.DataFrame, ref_df: pd.DataFrame) -> pd.DataFrame:
        '''

        Parameters
        ----------
        tar_df: pd.DataFrame, researcher division dataframe for matching
        ref_df: pd.DataFrame, rest division dataframe

        This function will use the sum of abs weight differences divided by the num of matched
        divisions to calculate the similarity between
        researchers.
        For instance, researcher A with division {a: 0.7, b: 0.3},
                      researcher B with division {a: 0.5, b: 0.2, c: 0.3},
                      researcher C with division {b: 0.9, d: 0.1},
        the matching result for A will be {B: (0.2+0.1)/2, C: 0.6/1}.
        One thing to note, the OTHERS(IRRELEVANT) division will be dropped.

        Returns
        -------
        pd.DataFrame, the matching result dataframe ordered by weight.
        '''

        tar_df = tar_df[tar_df['value'] != 'OTHERS(IRRELEVANT)']
        ref_df = ref_df[ref_df['value'] != 'OTHERS(IRRELEVANT)']

        norm_tar_df = tar_df.groupby(self.pk).apply(lambda x: normalize(x, 'weight'))
        norm_ref_df = ref_df.groupby(self.pk).apply(lambda x: normalize(x, 'weight'))

        merge_df = norm_ref_df.merge(norm_tar_df[['value', 'weight']], on='value')
        merge_df['weight'] = abs(merge_df['weight_x'] - merge_df['weight_y'])

        merge_df = weighted_avg(merge_df, self.pk, 'value')

        if merge_df.empty:
            return merge_df
        return merge_df[[self.pk, 'weight']].drop_duplicates()

    def __weighted_tag_sim(self, tar_df: pd.DataFrame, ref_df: pd.DataFrame) -> pd.DataFrame:
        '''

        Parameters
        ----------
        tar_df: pd.DataFrame, researcher tag dataframe for matching
        ref_df: pd.DataFrame, rest tag dataframe

        This function will use the weighted sum of tags to calculate the similarity between researchers.
        For instance, researcher A with tag {a: 0.7, b: 0.3},
                      researcher B with tag {a: 0.5, b: 0.2, c: 0.3},
                      researcher C with tag {b: 0.9, d: 0.1},
        the matching result for A will be {B: 0.35+0.06, C: 0.27}.
        One thing to note, the OTHERS(IRRELEVANT) division will be dropped.

        Returns
        -------
        pd.DataFrame, the matching result dataframe ordered by weight.
        '''

        tar_df = tar_df[tar_df['value'] != 'OTHERS(IRRELEVANT)'][[self.pk, 'Tag', 'weight']]
        ref_df = ref_df[ref_df['value'] != 'OTHERS(IRRELEVANT)'][[self.pk, 'Tag', 'weight']]

        tar_df = tar_df.groupby(self.pk).apply(lambda x: normalize(x, 'weight'))
        ref_df = ref_df.groupby(self.pk).apply(lambda x: normalize(x, 'weight'))

        candidate_df = ref_df[ref_df['Tag'].isin(tar_df['Tag'])]
        candidate_df = candidate_df.merge(tar_df, on='Tag', suffixes=('', '_x'))

        candidate_df['weight'] = abs(candidate_df['weight'] * candidate_df['weight_x'])
        candidate_df = candidate_df.groupby(self.pk)['weight'].sum().reset_index()
        return candidate_df

    def __combined_measure(self, div_list: List[pd.DataFrame], tag_list: List[pd.DataFrame]) -> pd.DataFrame:
        '''

        Parameters
        ----------
        div_list: List[pd.DataFrame], list of division dataframe
        tag_list: List[pd.DataFrame], list of tag dataframe

        Returns
        -------

        '''

        tmp_df1 = self.__weighted_div_sim(*div_list)
        if not tag_list[0].empty:
            tmp_df2 = self.__weighted_tag_sim(*tag_list)
            tmp_df1 = tmp_df1.merge(tmp_df2, on=self.pk, how='outer')
            tmp_df1['weight_x'].fillna(np.mean(tmp_df1['weight_x']))
            tmp_df1['weight_y'].fillna(np.mean(tmp_df1['weight_y']))
            del tmp_df2
            tmp_df1['weight'] = tmp_df1['weight_x'] - 2 * tmp_df1['weight_y']
        return tmp_df1.sort_values('weight')[[self.pk, 'weight']]

    def prepare_dataset(self, researcher_id: str) -> tuple[list, list]:

        '''

        Parameters
        ----------
        researcher_id: str, input researcher id for matching
        tags: List[str], list of tags if the researcher has, default as None

        This function will generate the dataset for later matching work. If input tag variable is
        not None, the new tag record will replace the old one for the input researcher(or create a new
        record if input researcher not exist). Otherwise the original dataset will be returned.

        Returns
        -------
        tuple[list, list],
        '''

        # Check if this researcher exist or if the tags are not None
        assert researcher_id in self.re_div_df[self.pk].unique(), f'No such researcher {self.pk}: {researcher_id}'

        tar_div_df = self.re_div_df[self.re_div_df[self.pk] == researcher_id]
        ref_div_df = self.re_div_df[self.re_div_df[self.pk] != researcher_id]

        tar_tag_df, ref_tag_df = pd.DataFrame(), pd.DataFrame()
        merged_tag_df = self.re_tag_df.merge(MAP_DF, on='Tag')

        if researcher_id in merged_tag_df[self.pk].unique():
            tar_tag_df = merged_tag_df[merged_tag_df[self.pk] == researcher_id]
            ref_tag_df = merged_tag_df[merged_tag_df[self.pk] != researcher_id]

        return [tar_div_df, ref_div_df], [tar_tag_df, ref_tag_df]

    # TODO: temp code
    def prepare_dataset_by_profile(self, divs: List[str], tags: List[str]) -> tuple[list, list]:
        '''

        Parameters
        ----------
        divs: List[str], list of divisions selected by user
        tags: List[str], list of tags selected by user

        Returns
        -------
        tuple[list, list],
        '''

        division_dict = {}
        for idx, div in enumerate(divs):
            division_dict[RESEARCH_FIELDS[div]['field']] = len(divs) - idx
        tar_div_df = pd.DataFrame({'Staff ID': 'current_tmp',
                                   'value': list(division_dict.keys()),
                                   'weight': list(division_dict.values())})

        tar_tag_df, ref_tag_df = pd.DataFrame(), pd.DataFrame()
        if tags and len(tags) != 0:
            tag_dict = {}
            for idx, tag in enumerate(tags):
                tag_dict[tag] = len(tags) - idx
            tar_tag_df = pd.DataFrame({'Name': 'current_tmp',
                                       'Staff ID': 'current_id',
                                       'Tag': list(tag_dict.keys()),
                                       'weight': list(tag_dict.values())})
            ref_tag_df = self.re_tag_df
            tar_tag_df = tar_tag_df.merge(MAP_DF, on='Tag')
            ref_tag_df = ref_tag_df.merge(MAP_DF, on='Tag')
        return [tar_div_df, self.re_div_df], [tar_tag_df, ref_tag_df]

    def __reformat_output(self, sim_df: pd.DataFrame, tar_col: List[str]) -> pd.DataFrame:
        '''

        Parameters
        ----------
        sim_df: pd.DataFrame, similar researcher dataframe
        tar_col: List[str], target info columns to extract

        This function will appending the similar researchers' info with his/her divisions and tags.

        Returns
        -------
        pd.DataFrame, similar researchers' info dataframe
        '''

        assert self.pk in sim_df.columns, 'Primary key is not in similar df.'

        info_df = INFO_DF[INFO_DF[self.pk].isin(sim_df[self.pk])][[self.pk] + tar_col]
        agg_tag_df = self.re_tag_df.groupby(self.pk)['Tag'].apply(lambda x: list(set(x))).reset_index()

        # filter other divisions out
        tmp_re_div = self.re_div_df[~self.re_div_df['value'].isin(['OTHERS(RELEVANT)', 'OTHERS(IRRELEVANT)'])]
        agg_div_df = tmp_re_div.groupby(self.pk)['value'].apply(lambda x: list(set(x))).reset_index()
        del tmp_re_div

        return info_df.merge(agg_tag_df, on=self.pk).merge(agg_div_df, on=self.pk).drop(self.pk, axis=1)

    def match_by_profile(self, divs: List[str], tags: List[str] = None, match_num=10, measure_func=__combined_measure):
        '''

        Parameters
        ----------
        divs: List[str], list of divisions selected by user, cannot be empty
        tags: List[str], list of tags selected by user, default as None
        match_num: int, defined how many matched researcher will be returned.
        measure_func: func, the measurement function for calculating similarity

        Returns
        -------
        List, info of similar researchers
        '''

        assert len(divs) != 0, 'At least the division should not be empty.'
        div_list, tag_list = self.prepare_dataset_by_profile(divs, tags)
        candidate_df = measure_func(self, div_list, tag_list)

        sim_df = candidate_df[:min(len(candidate_df), match_num)]
        sim_df = self.__reformat_output(sim_df, ['Name', 'Email', 'Colleges'])

        return sim_df.to_dict(orient='records')

    def match_by_id(self, researcher_id: str, match_num=10, measure_func=__combined_measure) -> pd.DataFrame:
        '''

        Parameters
        ----------
        researcher_id: str, input researcher id for matching.
        match_num: int, defined how many matched researcher will be returned.
        measure_func: func, the measurement function for calculating similarity

        Returns
        -------
        pd.DataFrame, dataframe of similar researchers
        '''

        div_list, tag_list = self.prepare_dataset(researcher_id)
        candidate_df = measure_func(self, div_list, tag_list)
        sim_df = candidate_df[:match_num]
        return sim_df

# if __name__ == '__main__':

# matching by divisions/tags
# rm = ResearcherMatcher()
# division_list = ['d_11', 'd_13']
# tag_list = ['health behavior', 'health services', 'Health Promotion']
# temp_df = rm.match_by_profile(division_list)
# print(temp_df)

# matching by id
# researcher_division_df = pd.read_csv(RESEARCHER_DIVISION_MAP_PATH)
# id_list = researcher_division_df['Staff ID'].unique().tolist()
# rm = ResearcherMatcher()
# save = []
# for i in range(21, 40):
#     sample_id = id_list[i]
#     print(sample_id)
#     temp_df = rm.match(sample_id)
#     temp_df['origin_staff'] = sample_id
#     save.append(temp_df)
#
# stuff_info_df = pd.read_csv(RESEARCHER_INFO_PATH)[['Staff ID', 'Colleges', 'Profile']]
# merge_df = pd.concat(save).merge(stuff_info_df, on='Staff ID').merge(stuff_info_df,
#                                                                      right_on='Staff ID',
#                                                                      left_on='origin_staff',
#                                                                      suffixes=('_match', '_orig'))
# merge_df.to_csv(RESEARCHER_MATCHING_OUTPUT, index=0, encoding='utf-8_sig')
