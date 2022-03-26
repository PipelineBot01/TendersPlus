import pandas as pd
from conf.file_path import RESEARCHER_DIVISION_MAP_PATH
from utils.match_utils import normalize

DIVISION_PATH = '../researcher/assets/' + RESEARCHER_DIVISION_MAP_PATH


def get_research_strength(div_path: str = DIVISION_PATH, pk='Staff ID') -> pd.DataFrame:
    '''

    Parameters
    ----------
    div_path: str, path for division data file
    pk: str, primary key for division dataframe, default as Staff ID.

    This function will generate the research strength for a university, final
    mark will be compressed to int(3~10)

    Returns
    -------
    pd.DataFrame, research strength for a university.
    '''
    div_df = pd.read_csv(div_path)
    div_df = div_df.groupby('value').agg({pk: 'count',
                                          'weight': 'sum'}).reset_index().sort_values('value').rename(
        columns={pk: 'count', 'weight': 'Total_weight'})
    div_df = div_df[~div_df['value'].isin(['OTHERS(RELEVANT)', 'OTHERS(IRRELEVANT)'])]
    div_df = normalize(div_df, 'Total_weight', method='rank')
    return div_df.to_dict(orient='records')
