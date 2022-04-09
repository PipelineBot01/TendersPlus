from conf.file_path import RESEARCHER_DIVISION_MAP_PATH, RESEARCHER_INFO_PATH, REG_RESEARCHER_INFO_PATH, \
    RESEARCHER_TAG_MAP_PATH, RESEARCHER_TAG_DIV_MAP_PATH
from db.loadjson import get_data
from db.mongodb import MongoConx
from db_conf import UNI_DATA
from researcher.clean.clean_data import data_clean
from researcher.features.researcher_feat_creator import ResearcherFeatCreator
from researcher.features.researcher_iter import ResearcherIter
from utils.feature_utils import get_user_profile


class ResearcherUpdater:
    def __init__(self,
                 info_path=RESEARCHER_INFO_PATH,
                 reg_info_path=REG_RESEARCHER_INFO_PATH,
                 researcher_tag_path=RESEARCHER_TAG_MAP_PATH,
                 researcher_div_path=RESEARCHER_DIVISION_MAP_PATH,
                 tag_div_map_path=RESEARCHER_TAG_DIV_MAP_PATH,
                 pk='id'):

        self.pk = pk
        self.__info_path = info_path
        self.__reg_info_path = reg_info_path
        self.researcher_tag_path = researcher_tag_path
        self.researcher_div_path = researcher_div_path
        self.tag_div_map_path = tag_div_map_path

        # get university info from mongo
        self.__mgx = MongoConx('staffs')
        raw_data_df = self.__mgx.read_df(UNI_DATA['UC'])
        self.__old_info_df, self.__old_tag_df = data_clean(raw_data_df, 'UC', pk)
        del raw_data_df

        self.ri = ResearcherIter(self.tag_div_map_path, self.researcher_div_path)
        self.rfc = ResearcherFeatCreator(self.researcher_tag_path, self.tag_div_map_path)

        self.__new_reg_info = get_data()
        self.__new_tag_df, self.__new_div_df, self.__new_tag_div_map_df = get_user_profile(self.__new_reg_info)

    def __update_researcher_info(self, info_df):
        info_df = self.__old_info_df.append(info_df)
        info_df = info_df.drop_duplicates(self.pk, keep='last')
        return info_df

    def __update_researcher_tag(self, tag_df):
        researcher_tag_map = self.__old_tag_df.append(tag_df)
        return researcher_tag_map

    def __update_researcher_div(self, div_df):
        researcher_div_map = self.rfc.create_researcher_division()
        researcher_div_map = researcher_div_map[~researcher_div_map[self.pk].isin(div_df[self.pk])]
        researcher_div_map = researcher_div_map.append(div_df)
        return researcher_div_map

    def update(self):
        # update info
        info_df = self.__update_researcher_info(self.__new_reg_info.drop(['divisions', 'tags'], axis=1))
        # TODO: will not run during testing
        # info_df.to_csv(self.__info_path, index=0)
        # self.__new_reg_info.to_csv(self.__reg_info_path, index=0)

        # update researcher-tag map
        self.__update_researcher_tag(self.__new_tag_df)
        # TODO: will not run during testing
        # researcher_tag_map.to_csv(self.researcher_tag_path, axis=0)

        # update researcher-div map
        self.__update_researcher_div(self.__new_div_df)
        # TODO: will not run during testing
        # researcher_div_map.to_csv(self.researcher_div_path, index=0)

        # update tag-div map
        tag_div_map_df = self.ri.fit_dataframe(self.__new_tag_div_map_df)
        # TODO: will not run during testing
        # tag_div_map_df.to_csv(self.tag_div_map_path, axis=0)
        print(tag_div_map_df)


if __name__ == '__main__':
    ru = ResearcherUpdater('../assets/researcher_info.csv',
                           '../assets/reg_researcher_info.csv',
                           '../assets/researcher_tag.csv',
                           '../assets/researcher_division.csv',
                           '../assets/tag_division_map.csv')
    ru.update()
