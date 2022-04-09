import pandas as pd

from conf.file_path import RESEARCHER_TAG_MAP_PATH, RESEARCHER_DIVISION_MAP_PATH, RESEARCHER_TAG_DIV_MAP_PATH


class ResearcherFeatCreator:
    def __init__(self,
                 tag_path=RESEARCHER_TAG_MAP_PATH,
                 div_path=RESEARCHER_DIVISION_MAP_PATH,
                 tag_div_map_path=RESEARCHER_TAG_DIV_MAP_PATH, pk='id'):
        self.pk = pk
        self.__tag_path = pd.read_csv(tag_path)
        self.__div_path = pd.read_csv(div_path)
        self.__tag_div_map = pd.read_csv(tag_div_map_path)

    def create_researcher_division(self) -> pd.DataFrame:
        merge_df = self.__tag_path.merge(self.__tag_div_map.drop('weight', axis=1), on='tag')
        merge_df = merge_df.groupby([self.pk, 'division']).agg({'weight': sum}).reset_index()
        return merge_df


if __name__ == '__main__':
    rfc = ResearcherFeatCreator('../assets/researcher_tag.csv',
                                '../assets/researcher_division.csv',
                                '../assets/tag_division_map.csv')
    print(rfc.create_researcher_division().columns)
