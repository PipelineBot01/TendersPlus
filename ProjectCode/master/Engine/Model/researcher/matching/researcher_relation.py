from typing import List
import pandas as pd, numpy as np
from conf.file_path import RESEARCHER_TAG_MAP_PATH, RESEARCHER_DIVISION_MAP_PATH, \
    RESEARCHER_TAG_CATE_MAP_PATH, RESEARCHER_MATCHING_OUTPUT, RESEARCHER_INFO_PATH
from relation_interface.Relation import Relation
from utils.match_utils import normalize, weighted_avg

MAP_DF = pd.read_csv(RESEARCHER_TAG_CATE_MAP_PATH)


class ResearcherMatcher(Relation):
    def __init__(self, re_div_df: pd.DataFrame, re_tag_df: pd.DataFrame, pk='Staff ID'):

        assert not re_div_df.empty, 'Cannot generate matcher due to empty file!'
        assert not (re_div_df.duplicated(pk).empty and re_tag_df.duplicated(pk).empty), \
            f'{pk} cannot be set as primary key!'

        self.re_div_df = re_div_df
        self.re_tag_df = re_tag_df
        self.pk = pk

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

        tar_df = tar_df[tar_df['value'] != 'DIVISION 24 OTHERS(IRRELEVANT)']
        ref_df = ref_df[ref_df['value'] != 'DIVISION 24 OTHERS(IRRELEVANT)']

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

        tar_df = tar_df[tar_df['value'] != 'DIVISION 24 OTHERS(IRRELEVANT)'][[self.pk, 'Tag', 'weight']]
        ref_df = ref_df[ref_df['value'] != 'DIVISION 24 OTHERS(IRRELEVANT)'][[self.pk, 'Tag', 'weight']]

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
        tar_list: List[pd.DataFrame], list of tar dataframe

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

    def prepare_dataset(self, researcher_id: str, tags=None) -> tuple[list, list]:

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

        if tags:
            tmp_df = pd.DataFrame({self.pk: [researcher_id], 'Tag': [tags]}).explode('Tag')
            tar_tag_df = tmp_df.merge(MAP_DF, on='Tag')
            ref_tag_df = merged_tag_df[merged_tag_df[self.pk] != researcher_id]

        return [tar_div_df, ref_div_df], [tar_tag_df, ref_tag_df]

    def match(self, researcher_id: str, match_num=10, tags=None, measure_func=__combined_measure) -> pd.DataFrame:
        '''

        Parameters
        ----------
        researcher_id: str, input researcher id for matching.
        match_num: int, how many matched researcher will be returned.
        tags: List[str], list of tags if the researcher has, default as None
        measure_func: relation measuring function

        Returns
        -------

        '''

        div_list, tag_list = self.prepare_dataset(researcher_id, tags)
        candidate_df = measure_func(self, div_list, tag_list)
        sim_df = candidate_df[:match_num]
        return sim_df


if __name__ == '__main__':

    researcher_division_df = pd.read_csv(RESEARCHER_DIVISION_MAP_PATH)
    researcher_tag_df = pd.read_csv(RESEARCHER_TAG_MAP_PATH)

    id_list = researcher_division_df['Staff ID'].unique().tolist()
    rm = ResearcherMatcher(researcher_division_df, researcher_tag_df)
    save = []
    for i in range(21, 40):
        sample_id = id_list[i]
        print(sample_id)
        temp_df = rm.match(sample_id)
        temp_df['origin_staff'] = sample_id
        save.append(temp_df)

    stuff_info_df = pd.read_csv(RESEARCHER_INFO_PATH)[['Staff ID', 'Colleges', 'Profile']]
    merge_df = pd.concat(save).merge(stuff_info_df, on='Staff ID').merge(stuff_info_df,
                                                                         right_on='Staff ID',
                                                                         left_on='origin_staff',
                                                                         suffixes=('_match', '_orig'))
    merge_df.to_csv(RESEARCHER_MATCHING_OUTPUT, index=0, encoding='utf-8_sig')
