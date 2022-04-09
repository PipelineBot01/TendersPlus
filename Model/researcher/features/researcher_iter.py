from typing import List

import pandas as pd

from conf.division import RESEARCH_FIELDS
from conf.file_path import RESEARCHER_TAG_DIV_MAP_PATH, RESEARCHER_DIVISION_MAP_PATH
from db.loadjson import get_data
from utils.match_utils import get_div_id_dict, normalize


class ResearcherIter:
    def __init__(self,
                 tag_div_map_path=RESEARCHER_TAG_DIV_MAP_PATH,
                 researcher_div_map_path=RESEARCHER_DIVISION_MAP_PATH, pk='id'):
        self.pk = pk
        self.__tag_div_map_path = tag_div_map_path
        self.__tag_div_map_df = pd.read_csv(self.__tag_div_map_path)

        self.__reg_user_df = get_data('user')
        self.__user_div_map = pd.read_csv(researcher_div_map_path)

        self.__user_div_map = self.__user_div_map[~self.__user_div_map['division'].isin(['OTHERS(IRRELEVANT)',
                                                                                         'OTHERS(RELEVANT)'])]
        div_dict = get_div_id_dict()
        self.__user_div_map['division'] = self.__user_div_map['division'].map(lambda x: div_dict[x])
        del div_dict

    def add_new_tags(self, div_list: List[str], tag_list: List[str]) -> pd.DataFrame:

        if div_list and len(div_list) != 0:
            tag_dict = {}
            for idx, tag in enumerate(div_list):
                tag_dict[tag] = len(div_list) - idx
        div_length = len(div_list)
        # new_tag_list = list(set(tag_list) - set(self.__tag_div_map_df['Tag'].unique().tolist()))
        new_tag_list = tag_list
        div_list = div_list * len(new_tag_list)
        new_tag_list = sorted(new_tag_list * div_length)
        tmp_df = pd.DataFrame({'tag': new_tag_list, 'division': div_list})
        tmp_df['weight'] = tmp_df['division'].map(lambda x: tag_dict[x]) / sum(tag_dict.values())
        self.__update_divs(tmp_df)

        # TODO: will not run during testing
        # self.__tag_div_map_df.to_csv(self.__tag_div_map_path)
        return self.__tag_div_map_df

    def __update_divs(self, new_tag_df: pd.DataFrame):
        tmp_df = self.__user_div_map.groupby('division')[self.pk].count().reset_index().rename(
            columns={self.pk: 'cnt'})
        new_tag_df = new_tag_df.merge(tmp_df)
        del tmp_df

        new_tag_df['weight'] = new_tag_df['weight'] / new_tag_df['cnt']
        new_tag_df['division'] = new_tag_df['division'].map(lambda x: RESEARCH_FIELDS[x]['field'])
        self.__tag_div_map_df = self.__tag_div_map_df.append(new_tag_df.drop('cnt', axis=1))
        # del new_tag_df

        self.__tag_div_map_df = self.__tag_div_map_df.groupby(['tag', 'division']).agg({'weight': sum}).reset_index()
        self.__tag_div_map_df = self.__tag_div_map_df.groupby(['tag']).apply(lambda x: normalize(x, 'weight'))
        print(self.__tag_div_map_df[self.__tag_div_map_df['tag'].isin(new_tag_df['tag'].unique())])
        del new_tag_df

ti = ResearcherIter('../assets/tag_division_map.csv', '../assets/researcher_division.csv')
ti.add_new_tags(['d_11', 'd_12', 'd_13'], ['ontology']*90)
