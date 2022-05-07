import pandas as pd
import sys
from conf.file_path import RESEARCHER_DIVISION_MAP_PATH
from utils.match_utils import normalize, get_div_id_dict
from typing import Dict, List


def get_research_strength(score_range: List[int] = [0, 10],
                          div_path: str = RESEARCHER_DIVISION_MAP_PATH, pk='id') -> Dict[str, dict]:
    '''
    Parameters
    ----------
    score_range: List[int, int]: range of score
    div_path: str, path for division data file
    pk: str, primary key for division dataframe, default as Staff ID.
    This function will generate the research strength for a university, final
    mark will be compressed to int(3~10)
    Returns
    -------
    dict[str, dict]
    '''

    div_df = pd.read_csv(div_path)
    div_df = div_df.groupby('division').agg({pk: 'count',
                                             'weight': 'sum'}).reset_index().sort_values('division').rename(
        columns={pk: 'count', 'weight': 'Total_weight'})
    div_df = div_df[~div_df['division'].isin(['OTHERS(RELEVANT)', 'OTHERS(IRRELEVANT)'])]
    div_df = normalize(div_df, 'Total_weight', method='rank', bounds=score_range)[['division', 'Total_weight']].rename(
        columns={'division': 'research_field', 'Total_weight': 'score'})
    div_id_dict = get_div_id_dict()
    div_df['research_field'] = div_df['research_field'].map(lambda x: div_id_dict[x])

    # TODO: hard code for university id  -2022/3/26 ray
    return {'u_01': div_df.to_dict(orient='records')}