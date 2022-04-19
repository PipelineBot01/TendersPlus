
from nltk.corpus import stopwords
import pandas as pd
from conf.features import PROJECT_STOP_WORDS
from conf.division import RESEARCH_FIELDS
import numpy as np
from utils.match_utils import normalize
from typing import Tuple

STOP_WORDS = stopwords.words('english')


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


def get_user_profile(input_df: pd.DataFrame, pk='id') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    '''

    Parameters
    ----------
    input_df
    pk

    Returns
    -------

    '''

    # generate div df
    input_df[pk] = 'Reg_' + input_df['email']
    div_df = input_df[[pk, 'divisions']].rename(columns={'divisions': 'division'}).copy()
    div_df = div_df.explode('division')
    div_df['division'] = div_df['division'].map(lambda x: RESEARCH_FIELDS[x]['field'])
    div_df = div_df.merge(
        div_df.groupby(pk)['division'].count().reset_index().rename(columns={'division': 'cnt'}))
    div_df['weight'] = 1 / div_df['cnt']
    div_df = div_df.groupby(pk).apply(lambda x: normalize(x, 'weight'))

    # generate tag df
    tag_df = input_df[[pk, 'tags']].rename(columns={'tags': 'tag'})
    tag_df = tag_df.explode('tag')
    tag_df = tag_df.replace('', np.nan)
    tag_df['tag'] = tag_df['tag'].str.lower()
    tag_df['weight'] = 1
    tag_df = tag_df.dropna()

    # generate div-tag map
    tag_div_map_df = div_df.drop('cnt', axis=1).merge(tag_df.drop('weight', axis=1), on=pk)

    return tag_df, div_df, tag_div_map_df
