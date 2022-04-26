from typing import Tuple, Dict, Union

from conf.file_path import RESEARCHER_TAG_MAP_PATH, RESEARCHER_DIVISION_MAP_PATH, \
    RESEARCHER_TAG_DIV_MAP_PATH, RESEARCHER_INFO_PATH
from utils.match_utils import *


class ResearcherMatcher:
    def __init__(self, re_div_path=RESEARCHER_DIVISION_MAP_PATH,
                 re_tag_path=RESEARCHER_TAG_MAP_PATH,
                 tag_div_path=RESEARCHER_TAG_DIV_MAP_PATH,
                 re_info_path=RESEARCHER_INFO_PATH, pk='id'):

        self.__re_div_path = re_div_path
        self.__re_tag_path = re_tag_path
        self.__tag_div_path = tag_div_path
        self.__re_info_path = re_info_path

        self.__re_div_df = pd.read_csv(self.__re_div_path)
        self.__re_tag_df = pd.read_csv(self.__re_tag_path)
        self.__MAP_DF = pd.read_csv(self.__tag_div_path).drop('weight', axis=1)
        self.__INFO_DF = pd.read_csv(self.__re_info_path)
        self.__pk = pk

        assert not self.__re_div_df.empty, 'Cannot generate matcher due to empty file!'
        assert not (self.__re_div_df.duplicated(pk).empty and self.__re_tag_df.duplicated(pk).empty), \
            f'{pk} cannot be set as primary key!'

    def __weighted_div_sim(self, tar_df: pd.DataFrame, ref_df: pd.DataFrame) -> pd.DataFrame:
        '''

        Parameters
        ----------
        tar_df: pd.DataFrame, researcher division dataframe for matching
        ref_df: pd.DataFrame, rest division dataframe

        This function will use the sum of abs weight differences divided by the num of matched
        divisions to calculate the similarity between researchers.
        For instance, researcher A with division {a: 0.7, b: 0.3},
                      researcher B with division {a: 0.5, b: 0.2, c: 0.3},
                      researcher C with division {b: 0.9, d: 0.1},
        the matching result for A will be {B: (0.2+0.1)/2, C: 0.6/1}.
        One thing to note, the OTHERS(IRRELEVANT) division will be dropped.

        Returns
        -------
        pd.DataFrame, the matching result dataframe ordered by weight.
        '''

        tar_df = tar_df[tar_df['division'] != 'OTHERS(IRRELEVANT)']
        ref_df = ref_df[ref_df['division'] != 'OTHERS(IRRELEVANT)']

        penalty_df = add_penalty_term(ref_df.copy(), self.__pk)
        ref_df = ref_df.merge(penalty_df)
        del penalty_df
        ref_df['weight'] = ref_df['weight'] * ref_df['penalty']

        norm_tar_df = tar_df.groupby(self.__pk).apply(lambda x: normalize(x, 'weight'))
        norm_ref_df = ref_df.groupby(self.__pk).apply(lambda x: normalize(x, 'weight'))
        del tar_df, ref_df

        merge_df = norm_ref_df.merge(norm_tar_df[['division', 'weight']], on='division')
        del norm_ref_df, norm_tar_df

        merge_df['weight'] = abs(merge_df['weight_x'] - merge_df['weight_y'])
        merge_df = weighted_avg(merge_df, self.__pk, 'division')

        if merge_df.empty:
            return merge_df
        return merge_df[[self.__pk, 'weight']].drop_duplicates()

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

        tar_df = tar_df[tar_df['division'] != 'OTHERS(IRRELEVANT)'][[self.__pk, 'tag', 'weight']]
        ref_df = ref_df[ref_df['division'] != 'OTHERS(IRRELEVANT)'][[self.__pk, 'tag', 'weight']]

        tar_df = tar_df.groupby(self.__pk).apply(lambda x: normalize(x, 'weight'))
        ref_df = ref_df.groupby(self.__pk).apply(lambda x: normalize(x, 'weight'))

        candidate_df = ref_df[ref_df['tag'].isin(tar_df['tag'])]
        candidate_df = candidate_df.merge(tar_df, on='tag', suffixes=('', '_x'))

        candidate_df['weight'] = abs(candidate_df['weight'] * candidate_df['weight_x'])
        candidate_df = candidate_df.groupby(self.__pk)['weight'].sum().reset_index()
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
            tmp_df1 = tmp_df1.merge(tmp_df2, on=self.__pk, how='outer')
            tmp_df1['weight_x'] = tmp_df1['weight_x'].fillna(np.mean(tmp_df1['weight_x']))
            tmp_df1['weight_y'] = tmp_df1['weight_y'].fillna(np.mean(tmp_df1['weight_y']))
            del tmp_df2
            tmp_df1['weight'] = tmp_df1['weight_x'] - 1.5 * tmp_df1['weight_y']
        tmp_df1.loc[tmp_df1['weight'] == 0, 'weight'] = 0.000001
        return tmp_df1.sort_values('weight')[[self.__pk, 'weight']]

    def __prepare_dataset(self, researcher_id: str) -> Tuple[list, list]:

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
        assert researcher_id in self.__re_div_df[self.__pk].unique(), f'No such researcher {self.__pk}: {researcher_id}'

        tar_div_df = self.__re_div_df[self.__re_div_df[self.__pk] == researcher_id]
        ref_div_df = self.__re_div_df[self.__re_div_df[self.__pk] != researcher_id]

        tar_tag_df, ref_tag_df = pd.DataFrame(), pd.DataFrame()
        merged_tag_df = self.__re_tag_df.merge(self.__MAP_DF, on='tag')

        if researcher_id in merged_tag_df[self.__pk].unique():
            tar_tag_df = merged_tag_df[merged_tag_df[self.__pk] == researcher_id]
            ref_tag_df = merged_tag_df[merged_tag_df[self.__pk] != researcher_id]

        return [tar_div_df, ref_div_df], [tar_tag_df, ref_tag_df]

    def __prepare_dataset_by_profile(self, id, divs: List[str], tags: List[str]) -> Tuple[list, list]:
        '''

        Parameters
        ----------
        divs: List[str], list of divisions selected by user
        tags: List[str], list of tags selected by user

        Returns
        -------
        tuple[list, list],
        '''

        division_dict = get_div_rank_dict(divs)
        tar_div_df = pd.DataFrame({self.__pk: 'current_tmp' if not id else id,
                                   'division': list(division_dict.keys()),
                                   'weight': list(division_dict.values())})

        tar_tag_df, ref_tag_df = pd.DataFrame(), pd.DataFrame()
        if tags and len(tags) != 0:
            tag_dict = {}
            for idx, tag in enumerate(tags):
                tag_dict[tag.lower()] = len(tags) - idx
            tar_tag_df = pd.DataFrame({'name': 'current_tmp',
                                       self.__pk: 'current_id',
                                       'tag': list(tag_dict.keys()),
                                       'weight': list(tag_dict.values())})
            ref_tag_df = self.__re_tag_df
            tar_tag_df = tar_tag_df.merge(self.__MAP_DF, on='tag')
            ref_tag_df = ref_tag_df.merge(self.__MAP_DF, on='tag')
        return [tar_div_df, self.__re_div_df], [tar_tag_df, ref_tag_df]

    def __reformat_output(self, sim_df: pd.DataFrame, tar_col: List[str], div_num=3, tag_num=10) -> pd.DataFrame:
        '''

        Parameters
        ----------
        sim_df: pd.DataFrame, similar researcher dataframe
        tar_col: List[str], target info columns to extract
        num: int, number of returned tags

        This function will appending the similar researchers' info with his/her divisions and tags.

        Returns
        -------
        pd.DataFrame, similar researchers' info dataframe
        '''

        assert self.__pk in sim_df.columns, 'Primary key is not in similar df.'

        info_df = self.__INFO_DF.merge(sim_df, on=self.__pk)[[self.__pk, 'weight'] + tar_col]
        info_df = info_df.fillna('')
        self.__re_tag_df = self.__re_tag_df.sort_values('weight', ascending=False)
        agg_tag_df = self.__re_tag_df.groupby(self.__pk).head(tag_num).groupby(self.__pk)['tag'].apply(
            lambda x: list(set(x))).reset_index()

        # filter other divisions out
        tmp_re_div = self.__re_div_df[
            ~self.__re_div_df['division'].isin(['OTHERS(RELEVANT)',
                                                'OTHERS(IRRELEVANT)'])].sort_values('weight', ascending=False)
        agg_div_df = tmp_re_div.groupby(self.__pk).head(div_num).groupby(self.__pk)['division'].apply(
            lambda x: list(set(x))).reset_index()
        del tmp_re_div

        return info_df.merge(agg_tag_df, on=self.__pk, how='left'
                             ).merge(agg_div_df, on=self.__pk, how='left').sort_values('weight')

    def update(self):
        self.__re_div_df = pd.read_csv(self.__re_div_path)
        self.__re_tag_df = pd.read_csv(self.__re_tag_path)
        self.__MAP_DF = pd.read_csv(self.__tag_div_path).drop('weight', axis=1)
        self.__INFO_DF = pd.read_csv(self.__re_info_path)

    def match_by_profile(self, profile_dict: Dict[str, Union[str, List[str]]],
                         match_num=10,
                         measure_func=__combined_measure,
                         get_dict=True,
                         remove_cur_id=True):
        '''

        Parameters
        ----------
        profile_dict: Dict[str, Union[str,List[str]]], in the form of
                id: the input user id
                divisions: List[str], list of divisions selected by user, cannot be empty
                tags: List[str], list of tags selected by user, default as None
        match_num: int, defined how many matched researcher will be returned.
        measure_func: func, the measurement function for calculating similarity
        get_dict: boolean, whether return a dictionary
        remove_cur_id: boolean, whether remove current user id
        Returns
        -------
        List, info of similar researchers
        '''

        id = profile_dict['id']
        divisions = profile_dict['divisions']
        tags = profile_dict['tags']
        assert len(divisions) != 0, 'At least the division should not be empty.'
        div_list, tag_list = self.__prepare_dataset_by_profile(id, divisions, tags)
        candidate_df = measure_func(self, div_list, tag_list)
        candidate_df = candidate_df[candidate_df['id'] != id] if remove_cur_id else candidate_df
        sim_df = candidate_df[:min(len(candidate_df), match_num)]
        sim_df = self.__reformat_output(sim_df, ['name', 'email', 'university'])

        if get_dict:
            sim_df = sim_df.to_dict(orient='records')
            for value in sim_df:
                if type(value['tag']) != type([]):
                    value['tag'] = []
        return sim_df

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

        div_list, tag_list = self.__prepare_dataset(researcher_id)
        candidate_df = measure_func(self, div_list, tag_list)

        # handle no enough matching result
        if len(candidate_df) < match_num:
            tmp_info_df = self.__INFO_DF[self.__INFO_DF[self.__pk] == researcher_id][[self.__pk]]
            other_df = self.__INFO_DF[self.__INFO_DF[self.__pk] != researcher_id][[self.__pk]]
            tmp_df = other_df[other_df['colleges'].isin(tmp_info_df['colleges'])].sample(frac=1)
            candidate_df = candidate_df.append(tmp_df)
            candidate_df['weight'] = candidate_df['weight'].fillna(
                np.mean(candidate_df[candidate_df['weight'].notna()]))
        sim_df = candidate_df[:match_num]
        return sim_df
