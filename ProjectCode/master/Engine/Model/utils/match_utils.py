import numpy as np
import pandas as pd


def normalize(input_df, target_col, method='proportion'):
    '''

    Parameters
    ----------
    input_df
    target_col
    method

    Returns
    -------

    '''
    assert method in ['proportion', 'max-min', 'rank'], f'{method} not in method list'
    if method == 'proportion':
        input_df[target_col] = input_df[target_col] / (input_df[target_col].sum())
    elif method == 'max-min':
        input_df[target_col] = (input_df[target_col] - input_df[target_col].min()
                                ) / (input_df[target_col].max() - input_df[target_col].min())
    elif method == 'rank':
        input_df[target_col] = 1 + 9 / (input_df[target_col].max() - input_df[target_col].min()) * (
                input_df[target_col] - input_df[target_col].min())
        input_df[target_col] = input_df[target_col].astype(int) * 2
        input_df.loc[input_df[target_col] < 3, target_col] = 3
        input_df.loc[input_df[target_col] > 10, target_col] = 10
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
    div_df = div_df[['Staff ID', 'value', 'penalty']]
    div_df['penalty'] = 1 - np.tanh(div_df['penalty'] / 10)
    return div_df
