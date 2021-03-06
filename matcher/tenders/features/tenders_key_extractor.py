import re
from typing import List, Tuple

import numpy as np
import pandas as pd
from keybert._model import KeyBERT
from nltk import pos_tag
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from utils.feature_utils import filter_words, PROJECT_STOP_WORDS

RE_SYMBOL = "[`~!@#$^&*()=|{}':;',\\[\\].<>/?~！@#￥……&*（）\-–——|{}【】‘’；：”“'。，、？%+_]"
RE_UPPER = '[A-Z0-9]{2,}'
RE_NUM_RULE = '\b(\d+|,)+\b'
RE_WEB_RULE = '[http|https]*://[a-zA-Z0-9.?/&=:-]*'
RE_URL_RULE = '[www|WWW]+\.[a-zA-Z0-9.?/&=:-]+'
RE_EMAIL_RULE = '[a-zA-Z0-9.?/&=:-]+@+[a-zA-Z0-9.?/&=:-]+'
RE_WEIGHT_RULE = '\((.*?)\)'

KW_MODEL = KeyBERT()
STOP = stopwords.words('english')


class KeyExtractor:
    def __init__(self):
        self.kw_model = KW_MODEL

    @staticmethod
    def remove_stopword(raw_df, col):
        raw_df[col] = raw_df[col].str.lower()
        raw_df[col] = raw_df[col].apply(lambda x: ' '.join(i for i in [item for item in x.split() if item not in STOP]))
        return raw_df

    def __preprocess(self, text: str) -> str:

        # Remove pure numbers, e.g., 2014, 20,000
        text = re.sub(RE_NUM_RULE, ' ', text)
        text = re.sub(RE_EMAIL_RULE, '', text)
        text = re.sub(RE_WEB_RULE, '', text)
        text = re.sub(RE_URL_RULE, '', text)
        text = re.sub(RE_SYMBOL, ' ', text)
        text = re.sub(RE_UPPER, '', text)
        return text.lower()

    def __split_words(self, x: pd.DataFrame) -> pd.DataFrame:
        x = x.replace('\'', '')
        return x.split()

    def __remove_keywords(self, row: pd.DataFrame) -> pd.DataFrame:
        reg_rule = r'\b(' + row["key"] + ')\\b'
        row['text'] = re.sub(reg_rule, ' ', row['text'])
        return row

    def __get_tags(self, df: pd.DataFrame) -> List[Tuple[str, float]]:
        '''

        Parameters
        ----------
        df: pd.DataFrame, input dataframe

        This function will call KeyBert to extract the keyword from text description of a
        tender, return a list with tuple[keyword, weight]. There are three keyword extraction
        strategies:
        1.  When the text description is intact, Maximal Marginal Relevance function with a low
            diversity value will be called to extract several similar keywords or phrases.
        2.  If above function return empty list, the normal keyword extraction function will be
            called to extract single key word from text.
        3.  If above two functions cannot extract any keyword, an empty tag "[none_tag]" will be
            returned.

        Returns
        -------
        List[Tuple[str, float]], list of key-weight tuples, with key as extracted keywords,
        weight as the assessed weight of the corresponding keyword.
        '''

        keywords = self.kw_model.extract_keywords(df['text'],
                                                  keyphrase_ngram_range=(1, 3),
                                                  stop_words='english',
                                                  use_mmr=True,
                                                  diversity=0.2)
        if len(keywords) == 0:
            keywords = self.kw_model.extract_keywords(df['text'], keyphrase_ngram_range=(1, 3), stop_words='english')
        return keywords if len(keywords) > 0 else [('[none_tag]', 1)]

    def __convert_word_type(self, text: str) -> str:
        # text = self.__preprocess(text)
        token = word_tokenize(text)
        lemmatizer = WordNetLemmatizer()
        pos_tagged = pos_tag(token)
        text = filter_words(pos_tagged, lemmatizer)
        return ' '.join(text)

    def __agg_tags(self, input_df: pd.DataFrame, target_col: str, pk: str) -> pd.DataFrame:
        '''

        Parameters
        ----------
        input_df: pd.DataFrame, input dataframe
        target_col: str, KeyBert result column for aggregation
        pk: str, name of the primary key for the input_df

        This function will count the total weight for each single word from
        tenders, according to the result by KeyBert. Weight from same word
        will be added and the one with the highest weight for each tenders
        will be returned as the candidate tag.

        Returns
        -------
        A dataframe with the shape of n*4. PKs are [items, key_orig]
        Columns: 'items': matching with each tenders project.
                 'key': extracted stem with the highest weight.
                 'value': total weight for the final stem
        '''

        input_df[target_col] = input_df[target_col].astype(str)

        # Extract and reformat term-weight set
        tmp_df = input_df[target_col].str.extractall(RE_WEIGHT_RULE).reset_index().set_index(pk)

        split_df = tmp_df[0].str.split(',', expand=True).rename(columns={0: 'key',
                                                                         1: 'value'})

        merge_df = tmp_df.merge(split_df, on=pk).drop(['match', 0], axis=1)
        del tmp_df, split_df

        merge_df['key'] = merge_df['key'].map(self.__split_words)
        mapping_df = merge_df.explode('key').reset_index()

        # Compute weight according to each word and ordering
        mapping_df['value'] = mapping_df['value'].astype(float)
        sum_df = mapping_df.groupby([pk, 'key'])['value'].sum().reset_index().sort_values('value', ascending=False)

        # Sampling top key
        removed_df = sum_df[~sum_df['key'].isin(PROJECT_STOP_WORDS)]
        removed_df = sum_df if sum_df.empty else removed_df

        key_df = removed_df.groupby(pk).head(1)[[pk, 'key']]
        return key_df

    def extract_label(self, input_df, pk: str, iteration_time: int) -> pd.DataFrame:
        '''

        Parameters
        ----------
        input_df: pd.DataFrame, input dataframe
        pk: str, name of the primary key for the input_df
        iteration_time: int, current iteration time

        Returns
        -------
        pd.DataFrame, output dataframe with the extracted key in this iteration and remained text col.
        '''

        # Get keywords in one around
        input_df['raw_result'] = input_df.apply(self.__get_tags, axis=1)

        # Aggregate keywords
        keyword_df = self.__agg_tags(input_df, 'raw_result', pk)

        first_df = input_df.reset_index()[[pk, 'text']].merge(keyword_df, how='left')

        # Generating new text
        input_df = input_df.drop('text', axis=1)
        first_df = first_df[first_df['key'].notna()].apply(self.__remove_keywords, axis=1).rename(
            columns={'key': f'key_{iteration_time}'})
        input_df = input_df.merge(first_df, on=pk, how='left')

        return input_df[[pk, f'key_{iteration_time}', 'text']]

    def __check_data_quality(self, input_df, pk):
        rows_null = input_df.isnull().sum(axis=1)
        print(f'---- tenders with less than 3 keywords {input_df[rows_null<3][pk].unique().tolist()}')

    def get_tags(self, input_df: pd.DataFrame, pk: str, text_col: str, iterations=16) -> pd.DataFrame:
        '''

        Parameters
        ----------
        input_df: pd.DataFrame,
        pk: str, name of the primary key for the input_df
        text_col: str, name of tenders' text description column
        iterations: iterations for extraction process

        This function will generate iteration times of keywords for each tender,
        keys may include empty value if KeyBert cannot extract any keyword from
        the text.

        Returns
        -------
        pd.DataFrame, original dataframe appending with key columns: [key_0, key_1 ...]
        '''

        assert text_col in input_df.columns, f'Missing column names "{text_col}".'
        tmp_df = input_df[input_df[text_col].notna()].copy()[[pk, text_col]]

        tmp_df[text_col] = tmp_df[text_col].map(lambda x: self.__preprocess(x))
        tmp_df[text_col] = tmp_df[text_col].map(lambda x: self.__convert_word_type(x))
        tmp_df = tmp_df.set_index(pk)[[text_col]]

        keys_col = []
        for i in range(iterations):
            print(f'---- start iteration {i}')
            tmp_df = self.extract_label(tmp_df, pk, i)
            input_df = input_df.drop('text', axis=1)
            input_df = input_df.merge(tmp_df[[pk, f'key_{i}', 'text']], on=pk, how='left')
            tmp_df = tmp_df[(tmp_df[f'key_{i}'] != '[none_tag]'
                             ) & (tmp_df['text'].notna())].drop(f'key_{i}', axis=1).set_index(pk)
            keys_col.append(f'key_{i}')
            if (tmp_df['text'].str.isspace()).all():
                break
            print(f'---- end iteration {i}')

        input_df = input_df.replace('[none_tag]', np.nan)[[pk] + keys_col]

        self.__check_data_quality(input_df, pk)
        return input_df
