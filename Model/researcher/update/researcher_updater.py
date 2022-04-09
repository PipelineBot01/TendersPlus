import pandas as pd
from database import UNI_DATA
from db.mongodb import MongoConx
from db.loadjson import get_data
from conf.division import RESEARCH_FIELDS
from researcher.clean.clean_data import data_clean
from conf.file_path import RESEARCHER_DIVISION_MAP_PATH, RESEARCHER_INFO_PATH, REG_RESEARCHER_INFO_PATH
from researcher.features.researcher_iter import ResearcherIter

class ResearcherUpdater:
    def __init__(self, region,
                 researcher_div_path = RESEARCHER_DIVISION_MAP_PATH,
                 info_path = RESEARCHER_INFO_PATH,
                 reg_info_path=REG_RESEARCHER_INFO_PATH,
                 pk='id'):
        self.pk = pk
        self.researcher_div_map = pd.read_csv(researcher_div_path)

        # get university info from mongo
        self.__mgx = MongoConx('staffs')
        raw_data_df = self.__mgx.read_df(UNI_DATA[region])
        self.__info_df, self.__tag_df = data_clean(raw_data_df, region, pk)
        del raw_data_df

        self.ri = ResearcherIter()

        self.__info_path = info_path
        self.__reg_info_path = reg_info_path


        self.__new_reg_info = get_data()
        self.__new_reg_info.rename(columns={'field_id':'division'}, inplace=True)
        self.__new_reg_info['field_id'] = self.__new_reg_info['field_id'].map(lambda x: RESEARCH_FIELDS[x]['field'])
        self.__new_reg_info[self.pk] = 'Reg_' + self.__new_reg_info['email']


    def __update_researcher_info(self):
        self.__info_df = self.__info_df.append(self.__reg_info)
        self.__info_df = self.__info_df.drop_duplicates(self.pk, keep='last')

        self.__info_df.to_csv(self.__info_path, index=0)
        self.__new_reg_info.to_csv(self.__reg_info_path, index=0)


    def __update_researcher_tag(self):
        tmp_df = self.__new_reg_info[[self.pk, 'division', 'tag']]
        new_tag_div_map = self.ri.add_new_tags(tmp_df['division'].values, tmp_df['tag'].values)
        self.__tag_df

    def update(self):



