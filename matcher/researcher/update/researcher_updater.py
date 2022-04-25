import re
import pandas as pd

from conf.file_path import RESEARCHER_DIVISION_MAP_PATH, RESEARCHER_INFO_PATH, REG_RESEARCHER_INFO_PATH, \
    RESEARCHER_TAG_MAP_PATH, RESEARCHER_TAG_DIV_MAP_PATH, RESEARCHER_ACTION_PATH
from db.loadjson import get_data
from db.mongodb import MongoConx
from db_conf import UNI_DATA
from researcher.clean.clean_data import data_clean
from researcher.features.researcher_feat_creator import ResearcherFeatCreator
from researcher.features.researcher_iter import ResearcherIter
from utils.feature_utils import get_user_profile

GOID_RULES = r'(GO[0-9]{4})'


class ResearcherUpdater:
    def __init__(self,
                 info_path=RESEARCHER_INFO_PATH,
                 reg_info_path=REG_RESEARCHER_INFO_PATH,
                 researcher_tag_path=RESEARCHER_TAG_MAP_PATH,
                 researcher_div_path=RESEARCHER_DIVISION_MAP_PATH,
                 tag_div_map_path=RESEARCHER_TAG_DIV_MAP_PATH,
                 action_path=RESEARCHER_ACTION_PATH,
                 pk='id'):
        self.pk = pk
        self.__info_path = info_path
        self.__reg_info_path = reg_info_path
        self.researcher_tag_path = researcher_tag_path
        self.researcher_div_path = researcher_div_path
        self.tag_div_map_path = tag_div_map_path
        self.action_path = action_path

        # get university info from mongo
        self.__mgx = MongoConx('staffs')
        raw_data_df = self.__mgx.read_df(UNI_DATA['UC'])
        self.__old_info_df, self.__old_tag_df = data_clean(raw_data_df, 'UC', pk)
        del raw_data_df

        self.__new_reg_info = get_data()
        self.__new_tag_df, self.__new_div_df, self.__new_tag_div_map_df = get_user_profile(self.__new_reg_info)

    def __extract_goid(self, row):
        result = re.findall(GOID_RULES, row)
        return result

    def __update_researcher_info(self, info_df):
        info_df = self.__old_info_df.append(info_df)
        info_df = info_df.drop_duplicates(self.pk, keep='last')
        return info_df

    def __update_researcher_tag(self, tag_df):
        researcher_tag_map = self.__old_tag_df.append(tag_df)
        return researcher_tag_map

    def __update_researcher_div(self, div_df):
        rfc = ResearcherFeatCreator(self.researcher_tag_path, self.tag_div_map_path)
        researcher_div_map = rfc.create_researcher_division()
        researcher_div_map = researcher_div_map[~researcher_div_map[self.pk].isin(div_df[self.pk])]
        researcher_div_map = researcher_div_map.append(div_df)
        return researcher_div_map

    def __update_researcher_action(self, action_df):
        action_df[self.pk] = 'Reg_' + action_df['email']
        action_df['go_id'] = action_df['payload'].map(self.__extract_goid)
        action_df['action_date'] = pd.to_datetime(action_df['action_date'])
        action_df = action_df.explode('go_id')[['id', 'type', 'action_date', 'go_id']]
        action_df.to_csv(self.action_path, index=0)

    def update(self):
        print('<start updating researcher files>')
        # update info
        print('-- start updating researcher info')
        info_df = self.__update_researcher_info(self.__new_reg_info.drop(['divisions', 'tags'], axis=1))
        info_df.to_csv(self.__info_path, index=0)
        self.__new_reg_info.to_csv(self.__reg_info_path, index=0)
        print('-- end updating researcher info')

        # update researcher-tag map
        print('-- start updating researcher tag map')
        researcher_tag_map = self.__update_researcher_tag(self.__new_tag_df)
        researcher_tag_map.to_csv(self.researcher_tag_path, index=0)
        print('-- end updating researcher tag map')

        # update researcher-div map
        print('-- start updating researcher div map')
        researcher_div_map = self.__update_researcher_div(self.__new_div_df)
        researcher_div_map.to_csv(self.researcher_div_path, index=0)
        print('-- start updating researcher div map')

        # update tag-div map
        print('-- start updating tag div map')
        ri = ResearcherIter(self.tag_div_map_path, self.researcher_div_path)
        tag_div_map_df = ri.fit_dataframe(self.__new_tag_div_map_df)
        tag_div_map_df.to_csv(self.tag_div_map_path, index=0)
        print('-- start updating tag div map')

        # update researcher action info
        print('-- start updating researcher action info')
        action_df = get_data('action')
        self.__update_researcher_action(action_df)
        print('-- end updating researcher action info')

        print('<end updating researcher files>')
