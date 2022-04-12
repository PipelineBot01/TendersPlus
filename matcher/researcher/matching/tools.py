import pandas as pd

from conf.division import RESEARCH_FIELDS
from conf.file_path import RESEARCHER_TAG_MAP_PATH, RESEARCHER_DIVISION_MAP_PATH, \
    RESEARCHER_TAG_DIV_MAP_PATH, RESEARCHER_INFO_PATH
for i in [RESEARCHER_TAG_MAP_PATH, RESEARCHER_DIVISION_MAP_PATH, RESEARCHER_TAG_DIV_MAP_PATH, RESEARCHER_INFO_PATH]:
    pd.read_csv(i.replace(' ', '').replace('_pickle', '.csv')).to_pickle(i)