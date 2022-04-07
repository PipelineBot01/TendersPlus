from typing import List

import pandas as pd
from conf.file_path import RESEARCHER_TAG_CATE_MAP_PATH
from utils.match_utils import normalize


class TendersIter:
    def __init__(self, tag_div_map_path=RESEARCHER_TAG_CATE_MAP_PATH):
        self.tag_div_map_df = pd.read_csv(tag_div_map_path)

    def add_new_tags(self, div_list: List[str], tag_list: List[str]):

        if div_list and len(div_list) != 0:
            tag_dict = {}
            for idx, tag in enumerate(div_list):
                tag_dict[tag] = len(div_list) - idx

        div_length = len(div_list)
        new_tag_list = list(set(tag_list) - set(self.tag_div_map_df['Tag'].unique().tolist()))
        div_list = div_list * len(new_tag_list)
        new_tag_list = sorted(new_tag_list * div_length)
        tmp_df = pd.DataFrame({'Tag': new_tag_list, 'value': div_list})
        tmp_df['weight'] = 1 / div_length
        self.tag_div_map_df = self.tag_div_map_df.append(tmp_df)
        return self.tag_div_map_df

    def update_divs(self):
        pass


ti = TendersIter('../assets/tag_category_map.csv')
ti.add_new_tags(['a', 'b', 'c'], [1,2,3])