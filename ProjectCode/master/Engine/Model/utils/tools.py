import pandas as pd
from conf.file_path import RESEARCHER_DIVISION_MAP_PATH
from utils.match_utils import normalize

DIVISION_PATH = '../researcher/assets/' + RESEARCHER_DIVISION_MAP_PATH


def get_research_strength(div_path: str = DIVISION_PATH, pk='Staff ID'):
    div_df = pd.read_csv(div_path)
    div_df = div_df.groupby('value').agg({pk: 'count',
                                          'weight': 'sum'}).reset_index().sort_values('value').rename(
        columns={pk: 'count', 'weight': 'Total_weight'})
    div_df = div_df[~div_df['value'].isin(['OTHERS(RELEVANT)', 'OTHERS(IRRELEVANT)'])]
    div_df = normalize(div_df, 'Total_weight', method='rank')
    return div_df


print(get_research_strength())
