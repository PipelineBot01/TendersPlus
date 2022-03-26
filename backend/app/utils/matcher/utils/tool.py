import pandas as pd
from typing import Dict
from .match import normalize, get_div_id_dict

DIVISION_PATH = 'utils/matcher/researcher/assets/researcher_division.csv'


def get_research_strength(div_path: str = DIVISION_PATH, pk='Staff ID') -> Dict[str, dict]:
    '''

    Parameters
    ----------
    div_path: str, path for division data file
    pk: str, primary key for division dataframe, default as Staff ID.

    This function will generate the research strength for a university, final
    mark will be compressed to int(3~10)

    Returns
    -------
    dict[str, dict]
    '''

    div_df = pd.read_csv(div_path)
    div_df = div_df.groupby('value').agg({pk: 'count',
                                          'weight': 'sum'}).reset_index().sort_values('value').rename(
        columns={pk: 'count', 'weight': 'Total_weight'})
    div_df = div_df[~div_df['value'].isin(['OTHERS(RELEVANT)', 'OTHERS(IRRELEVANT)'])]
    div_df = normalize(div_df, 'Total_weight', method='rank')[['value', 'Total_weight']].rename(
        columns={'value': 'research_field', 'Total_weight': 'score'})

    div_id_dict = get_div_id_dict()
    div_df['research_field'] = div_df['research_field'].map(lambda x: div_id_dict[x])

    # TODO: hard code for university id  -2022/3/26 ray
    return {'u_01': div_df.to_dict(orient='records')}
