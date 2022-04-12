from typing import List

import pandas as pd

from conf.division import RESEARCH_FIELDS
from conf.file_path import RESEARCHER_TAG_DIV_MAP_PATH, RESEARCHER_DIVISION_MAP_PATH
from db.loadjson import get_data
from utils.feature_utils import get_user_profile
from utils.match_utils import get_div_id_dict, normalize


class ResearcherIter:
    def __init__(self,
                 tag_div_map_path=RESEARCHER_TAG_DIV_MAP_PATH,
                 researcher_div_map_path=RESEARCHER_DIVISION_MAP_PATH, pk='id'):
        self.pk = pk
        self.__tag_div_map_path = tag_div_map_path
        self.__tag_div_map_df = pd.read_csv(self.__tag_div_map_path)

        tag_df, div_df, _ = get_user_profile(get_data('user'))
        div_df = div_df[div_df[self.pk].isin(tag_df[self.pk])]

        self.div_cnt_df = div_df.groupby('division')[self.pk].count().reset_index().rename(columns={self.pk: 'cnt'})
        del tag_df, div_df

        self.__user_div_map = pd.read_csv(researcher_div_map_path)

        self.__user_div_map = self.__user_div_map[~self.__user_div_map['division'].isin(['OTHERS(IRRELEVANT)',
                                                                                         'OTHERS(RELEVANT)'])]
        # div_dict = get_div_id_dict()
        # self.__user_div_map['division'] = self.__user_div_map['division'].map(lambda x: div_dict[x])
        # del div_dict

    def fit_list(self, div_list: List[str], tag_list: List[str]) -> pd.DataFrame:
        div_length = len(div_list)
        # new_tag_list = list(set(tag_list) - set(self.__tag_div_map_df['Tag'].unique().tolist()))
        new_tag_list = tag_list
        div_list = div_list * len(new_tag_list)
        new_tag_list = sorted(new_tag_list * div_length)
        tmp_df = pd.DataFrame({'tag': new_tag_list, 'division': div_list})
        tmp_df = tmp_df.merge(
            tmp_df.groupby('tag')['division'].count().reset_index().rename(columns={'division': 'cnt'}))
        tmp_df['weight'] = 1 / tmp_df['cnt']

        tmp_df['division'] = tmp_df['division'].map(lambda x: RESEARCH_FIELDS[x]['field'])
        tag_div_map_df = self.__update_divs(tmp_df.drop('cnt', axis=1))

        # TODO: will not run during testing
        # tag_div_map_df.to_csv(self.__tag_div_map_path)
        return tag_div_map_df

    def fit_dataframe(self, input_df: pd.DataFrame) -> pd.DataFrame:
        tag_div_map_df = self.__update_divs(input_df)

        # TODO: will not run during testing
        # self.tag_div_map_df.to_csv(self.__tag_div_map_path)
        return tag_div_map_df

    def __update_divs(self, new_tag_df: pd.DataFrame) -> pd.DataFrame:
        tmp_df = self.__user_div_map.groupby('division')[self.pk].count().reset_index().rename(
            columns={self.pk: 'cnt'})
        new_tag_df = new_tag_df.merge(tmp_df, on='division')
        del tmp_df

        new_tag_df = new_tag_df.merge(self.div_cnt_df, suffixes=('', '_new'), on='division')
        assert not new_tag_df.empty, 'input tags are not contained in user data'

        new_tag_df['weight'] = new_tag_df['weight'] / (new_tag_df['cnt'] / 2 + new_tag_df['cnt_new'])
        tag_div_map_df = self.__tag_div_map_df.append(new_tag_df.drop('cnt', axis=1))
        # del new_tag_df

        tag_div_map_df = tag_div_map_df.groupby(['tag', 'division']).agg({'weight': sum}).reset_index()
        tag_div_map_df = tag_div_map_df.groupby(['tag']).apply(lambda x: normalize(x, 'weight'))
        print(tag_div_map_df[tag_div_map_df['tag'].isin(new_tag_df['tag'].unique())])

        return tag_div_map_df



if __name__ == '__main__':
    ti = ResearcherIter('../assets/tag_division_map.csv', '../assets/researcher_division.csv')
    ti.fit_list(['d_05', 'd_06', 'd_04'], ['ontology'] * 90)
