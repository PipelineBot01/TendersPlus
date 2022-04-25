from typing import List

import numpy as np
import pandas as pd

from conf.division import RESEARCH_FIELDS


def get_div_rank_dict(div_list: List[str], is_weighted=False):
    division_dict = {}
    for idx, div in enumerate(div_list):
        division_dict[RESEARCH_FIELDS[div]['field']] = len(div_list) - idx if is_weighted else 1
    return division_dict


def get_div_id_dict():
    div_id_dict = {}
    for _id in RESEARCH_FIELDS.keys():
        div_id_dict[RESEARCH_FIELDS[_id]['field']] = _id
    return div_id_dict


def get_proportion(row):
    if row.notna().all():
        row['tmp'] = min(abs(row['weight']), abs(row['tmp'])) / max(abs(row['weight']), abs(row['tmp']))
    return row


def normalize(input_df, target_col, method='proportion', bounds=[0, 1]):
    '''

    Parameters
    ----------
    input_df
    target_col
    method
    bounds

    Returns
    -------

    '''
    assert method in ['proportion', 'max_min', 'scaled_max_min', 'rank'], f'{method} not in method list'
    if method == 'proportion':
        input_df[target_col] = input_df[target_col] / (input_df[target_col].sum())

    elif method == 'max_min':
        input_df[target_col] = (input_df[target_col] - input_df[target_col].min()
                                ) / (input_df[target_col].max() - input_df[target_col].min())

    elif method == 'scaled_max_min':
        if input_df[target_col].nunique() == 1:
            return input_df
        input_df = input_df.sort_values(target_col).reset_index(drop=True)
        input_df['tmp'] = input_df[target_col].shift(-1)
        input_df = input_df.apply(lambda x: get_proportion(x), axis=1)
        input_df[target_col] = (input_df[target_col] - input_df[target_col].min()
                                ) / (input_df[target_col].max() - input_df[target_col].min())

        input_df.loc[0, target_col] = input_df.iloc[1][target_col] * input_df.iloc[0]['tmp']
        input_df.loc[len(input_df) - 1, target_col] = input_df.iloc[-2][target_col] / input_df.iloc[-2]['tmp']

        input_df = input_df.drop('tmp', axis=1)

    elif method == 'rank':
        if input_df[target_col].nunique() == 1:
            input_df[target_col] = np.mean(bounds)
            return input_df
        input_df[target_col] = (bounds[0] + 1) + (bounds[1] - 1) / (
                input_df[target_col].max() - input_df[target_col].min()) * (
                                       input_df[target_col] - input_df[target_col].min())
        input_df[target_col] = input_df[target_col].astype(int) * 2
        input_df.loc[input_df[target_col] < 0.3 * (bounds[0] + bounds[1]), target_col] = 0.3 * (bounds[0] + bounds[1])
        input_df.loc[input_df[target_col] > bounds[1], target_col] = bounds[1]
    return input_df


def weighted_avg(merge_df: pd.DataFrame, pk, count_col) -> pd.DataFrame:
    '''

    Parameters
    ----------
    merge_df
    pk
    count_col

    Returns
    -------

    '''
    cnt_df = merge_df.groupby(pk)[count_col].count().reset_index().rename(columns={count_col: 'cnt'})
    merge_df = merge_df.groupby(pk)['weight'].sum().reset_index()
    merge_df = merge_df.merge(cnt_df, on=pk)
    merge_df['weight'] = merge_df['weight'] / merge_df['cnt']
    return merge_df


def add_penalty_term(div_df: pd.DataFrame, pk: str, ref_col: str = 'weight') -> pd.DataFrame:
    '''

    Parameters
    ----------
    div_df: pd.DataFrame, input division dataframe
    pk: primary key for div_df
    ref_col: reference column for generating penalty term

    This func will add penalty term to each researcher.
    For instance, a researcher with division and weight [div_a: 0.4, div_b: 0.3, div_c: 0.3]
    will be appended with penalty terms [div_a_pt: 1-tanh(0), div_b: 1-tanh(1/10), div_c: 1-tanh(1/10)]
    Returns
    -------
    pd.DataFrame, dataframe with cols of Staff ID, value, penalty
    '''

    div_df['penalty'] = 0
    div_df = div_df.sort_values(ref_col, ascending=False)
    div_df[f'{ref_col}_next'] = div_df.groupby(pk)[ref_col].shift(1)

    cond = div_df[f'{ref_col}_next'].notna()
    div_df.loc[cond & (div_df[f'{ref_col}_next'] > div_df[ref_col]), 'penalty'] = 1
    div_df['penalty'] = div_df.groupby(pk)['penalty'].cumsum()
    div_df = div_df[['id', 'division', 'penalty']]
    div_df['penalty'] = 1 - np.tanh(div_df['penalty'] / 10)
    return div_df
