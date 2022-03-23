import pandas as pd
from nltk.corpus import stopwords
from conf.stop_words import PROJECT_STOP_WORDS

STOP_WORDS = stopwords.words('english')

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


def filter_words(pos_tagged, lemmatizer):
    '''

    Parameters
    ----------
    pos_tagged
    lemmatizer

    Returns
    -------

    '''
    words = []
    noun = list(filter(
        lambda x: x[0] not in STOP_WORDS and (x[1].startswith('NN') or x[1].startswith('JJ')),
        pos_tagged))
    for word, pos in noun:
        if pos.startswith('NN'):
            word = lemmatizer.lemmatize(word, pos='n')
        elif pos.startswith('JJ'):
            word = lemmatizer.lemmatize(word, pos='a')
        if word not in PROJECT_STOP_WORDS:
            words.append(word)
    return words

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
