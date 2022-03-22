import re
from typing import List, Tuple
import nltk
import numpy as np, pandas as pd
from keybert._model import KeyBERT
from utils.match_utils import filter_words, PROJECT_STOP_WORDS

RE_SYMBOL = "[`~!@#$^&*()=|{}':;',\\[\\].<>/?~！@#￥……&*（）\-–——|{}【】‘’；：”“'。，、？%+_]"
RE_UPPER = '[A-Z]{2,}'
RE_WEIGHT_RULE = r'\((.*?)\)'

KW_MODEL = KeyBERT()

class KeyExtractor:
    def __init__(self):
        self.kw_model = KW_MODEL

    def __preprocess(self, text: str) -> str:
        text = re.sub(RE_SYMBOL, ' ', text)
        text = re.sub(RE_UPPER, '', text)
        return text.lower()

    def __split_words(self, x: pd.DataFrame) -> pd.DataFrame:
        x = x.replace('\'', '')
        return x.split()

    def __remove_keywords(self, row: pd.DataFrame) -> pd.DataFrame:
        row['text'] = row['text'].replace(row['key'], '')
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
        text = self.__preprocess(text)
        token = nltk.word_tokenize(text)
        lemmatizer = nltk.stem.WordNetLemmatizer()
        pos_tagged = nltk.pos_tag(token)
        text = filter_words(pos_tagged, lemmatizer)
        return ' '.join(text)

    def __agg_tags(self, input_df: pd.DataFrame, target_col: str) -> pd.DataFrame:
        '''

        Parameters
        ----------
        input_df: pd.DataFrame, input dataframe
        target_col: str, KeyBert result column for aggregation,

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
        tmp_df = input_df[target_col].str.extractall(RE_WEIGHT_RULE).reset_index().reset_index()
        split_result = tmp_df[0].str.split(',', expand=True).rename(columns={0: 'key',
                                                                             1: 'value'}).reset_index()

        merge_df = tmp_df.merge(split_result, on='index').drop('index', axis=1).rename(columns={'level_0': 'items'})
        del tmp_df, split_result

        merge_df['key'] = merge_df['key'].map(self.__split_words)
        mapping_df = merge_df.explode('key')[['items', 'key', 'value']]

        # Compute weight according to each word and ordering
        mapping_df['value'] = mapping_df['value'].astype(float)
        sum_df = mapping_df.groupby(['items', 'key'])['value'].sum().reset_index().sort_values(
            ['items', 'value'], ascending=False)

        # Sampling top key
        removed_df = sum_df[~sum_df['key'].isin(PROJECT_STOP_WORDS)]
        removed_df = sum_df if sum_df.empty else removed_df

        key_df = removed_df.groupby(['items']).head(1)[['items', 'key']]
        merge_df = sum_df.merge(key_df, on=['items', 'key'])

        return merge_df

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
        merge_df = self.__agg_tags(input_df, 'raw_result')
        first_df = input_df[['index', 'text']].merge(merge_df, left_on='index', right_on='items', how='left')

        # Generating new text
        df = input_df.drop('text', axis=1)
        first_df = first_df[first_df['key'].notna()].apply(self.__remove_keywords, axis=1).rename(
            columns={'key': f'key_{iteration_time}'}).drop('items', axis=1)
        df = df.merge(first_df, on='index', how='left')

        return df[[pk, f'key_{iteration_time}', 'text']]

    def get_tags(self, input_df: pd.DataFrame, pk: str, text_col: str, iterations=10) -> pd.DataFrame:
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
        tmp_df = input_df[input_df[text_col].notna()].copy()
        tmp_df[text_col] = tmp_df[text_col].map(lambda x: self.__preprocess(x))
        tmp_df[text_col] = tmp_df[text_col].map(lambda x: self.__convert_word_type(x))

        # Remove pure numbers, e.g., 2014, 20,000
        tmp_df[text_col] = tmp_df[text_col].map(lambda x: re.sub(r'\s*(\.:,|\d+)\s*', '', x))
        tmp_df = tmp_df.reset_index(drop=True).reset_index()
        tmp_df = tmp_df[[pk, text_col, 'index']]

        for i in range(iterations):
            tmp_df = self.extract_label(tmp_df, pk, i)
            input_df['text'] = tmp_df['text'].copy()
            input_df = input_df.merge(tmp_df[['_id', f'key_{i}']], on=pk, how='left')
            tmp_df = tmp_df[(tmp_df[f'key_{i}'] != '[none_tag]') & (tmp_df['text'].notna())].reindex().reset_index()

        input_df = input_df.replace('[none_tag]', np.nan)
        return input_df


if __name__ == '__main__':
    input_df = pd.read_csv('../assets/tenders_info.csv')
    input_df['text'] = input_df['Description'] + '.' + input_df['Title']
    ke = KeyExtractor()
    re_df = ke.get_tags(input_df[:10], '_id', 'text')
    re_df.to_csv('remove_num_tenders.csv', index=0, encoding='utf-8_sig')
