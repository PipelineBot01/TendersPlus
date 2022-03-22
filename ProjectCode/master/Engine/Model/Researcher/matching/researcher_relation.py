import pandas as pd
from utils.match_utils import normalize

MAP_DF = pd.read_csv('../assets/tag_category_map.csv')


class ResearcherMatcher:

    def __init__(self, re_div_df: pd.DataFrame, re_tag_df: pd.DataFrame, pk='Staff ID'):

        assert not re_div_df.empty, 'Cannot generate matcher due to empty file!'
        assert not (re_div_df.duplicated(pk).empty and re_tag_df.duplicated(pk).empty), \
            f'{pk} cannot be set as primary key!'

        self.re_div_df = re_div_df
        self.re_tag_df = re_tag_df
        self.pk = pk

    def __weighted_avg(self, input_df: pd.DataFrame) -> pd.DataFrame:
        input_df['Weight'] = input_df['Weight'].sum() / len(input_df['value'].unique())
        return input_df

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

        norm_tar_df = tar_df.groupby(self.pk).apply(lambda x: normalize(x, 'Weight'))
        norm_ref_df = ref_df.groupby(self.pk).apply(lambda x: normalize(x, 'Weight'))

        merge_df = norm_ref_df.merge(norm_tar_df[['value', 'Weight']], on='value')
        merge_df['Weight'] = abs(merge_df['Weight_x'] - merge_df['Weight_y'])
        merge_df = merge_df.groupby(self.pk).apply(lambda x: self.__weighted_avg(x))
        if merge_df.empty:
            return merge_df
        return merge_df[[self.pk, 'Weight']].drop_duplicates()

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

        tar_df = tar_df[tar_df['value'] != 'DIVISION 24 OTHERS(IRRELEVANT)'][[self.pk, 'Tags', 'Weight']]
        ref_df = ref_df[ref_df['value'] != 'DIVISION 24 OTHERS(IRRELEVANT)'][[self.pk, 'Tags', 'Weight']]

        tar_df = tar_df.groupby(self.pk).apply(lambda x: normalize(x, 'Weight'))
        ref_df = ref_df.groupby(self.pk).apply(lambda x: normalize(x, 'Weight'))

        candidate_df = ref_df[ref_df['Tags'].isin(tar_df['Tags'])]
        candidate_df = candidate_df.merge(tar_df, on='Tags', suffixes=('', '_x'))

        candidate_df['Weight'] = abs(candidate_df['Weight'] * candidate_df['Weight_x'])
        candidate_df = candidate_df.groupby(self.pk)['Weight'].sum().reset_index()
        return candidate_df

    def __combined_measure(self, div_list, tar_list):
        tmp_df1 = self.__weighted_div_sim(*div_list)
        if not tar_list[0].empty:
            tmp_df2 = self.__weighted_tag_sim(*tar_list)
            tmp_df1 = tmp_df1.merge(tmp_df2, on='Staff ID')
            del tmp_df2
            tmp_df1['Weight'] = tmp_df1['Weight_x'] - 2 * tmp_df1['Weight_y']
        return tmp_df1.sort_values('Weight')[[self.pk, 'Weight']]

    def prepare_dataset(self, researcher_id: pd.DataFrame, tags=None):

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
        pd.DataFrame, dataset for later matching work
        '''

        # Check if this researcher exist or if the tags are not None
        assert researcher_id in self.re_div_df[self.pk].unique(), f'No such researcher {self.pk}: {researcher_id}'

        tar_div_df = self.re_div_df[self.re_div_df[self.pk] == researcher_id]
        ref_div_df = self.re_div_df[self.re_div_df[self.pk] != researcher_id]

        tar_tag_df, ref_tag_df = pd.DataFrame(), pd.DataFrame()
        merged_tag_df = self.re_tag_df.merge(MAP_DF, on='Tags')

        if researcher_id in merged_tag_df[self.pk].unique():
            tar_tag_df = merged_tag_df[merged_tag_df[self.pk] == researcher_id]
            ref_tag_df = merged_tag_df[merged_tag_df[self.pk] != researcher_id]

        if tags:
            tmp_df = pd.DataFrame({self.pk: [researcher_id], 'Tags': [tags]}).explode('Tags')
            tar_tag_df = tmp_df.merge(MAP_DF, on='Tags')
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

        div_list, tar_list = self.prepare_dataset(researcher_id, tags)
        candidate_df = measure_func(self, div_list, tar_list)
        sim_df = candidate_df[:match_num]
        return sim_df


if __name__ == '__main__':

    researcher_division_df = pd.read_csv('../assets/researcher_division.csv')
    researcher_tag_df = pd.read_csv('../assets/researcher_tag.csv')

    id_list = researcher_division_df['Staff ID'].unique().tolist()
    rm = ResearcherMatcher(researcher_division_df, researcher_tag_df)
    save = []
    for i in range(21, 40):
        sample_id = id_list[i]
        print(sample_id)
        temp_df = rm.match(sample_id)
        temp_df['origin_staff'] = sample_id
        save.append(temp_df)

    stuff_info_df = pd.read_csv('staffs_info.csv')[['Staff ID', 'Colleges', 'Profile']]
    merge_df = pd.concat(save).merge(stuff_info_df, on='Staff ID').merge(stuff_info_df,
                                                                         right_on='Staff ID',
                                                                         left_on='origin_staff',
                                                                         suffixes=('_match', '_orig'))
    merge_df.to_csv('researcher_match_result.csv', index=0, encoding='utf-8_sig')
