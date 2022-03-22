import re
from typing import List, Tuple
import nltk
import numpy as np
import pandas as pd
from keybert._model import KeyBERT
from nltk.corpus import stopwords


class KeyExtractor:
    def __init__(self):
        self.STOP_WORDS = stopwords.words('english')
        self.kw_model = KeyBERT()

    def __split_words(self, x: pd.DataFrame) -> pd.DataFrame:
        x = x.replace('\'', '')
        return x.split()

    def __remove_keywords(self, row: pd.DataFrame) -> pd.DataFrame:
        for key in row['key_orig']:
            row['text'] = row['text'].replace(key, '')
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

    def __convert_word_type(self, word):
        token = nltk.word_tokenize(str(word).lower())
        lemmatizer = nltk.stem.WordNetLemmatizer()
        pos_tagged = nltk.pos_tag(token)
        words = []
        Noun = list(filter(
            lambda x: x[0] not in self.STOP_WORDS and x[0] != '/' and (x[1].startswith('NN') or x[1].startswith('JJ')),
            pos_tagged))
        for word, pos in Noun:
            if pos.startswith('NN'):
                word = lemmatizer.lemmatize(word, pos='n')
            elif pos.startswith('JJ'):
                word = lemmatizer.lemmatize(word, pos='a')
            words.append(word)
        text = " ".join(words)
        return text

    def __agg_tags(self, input_df: pd.DataFrame, target_col: str) -> pd.DataFrame:
        '''

        Parameters
        ----------
        input_df: pd.DataFrame, input dataframe
        target_col: str, KeyBert result column for aggregation,

        This function will count the total weight for each single stem by
        tenders, according to the result from KeyBert. Weight from same stem
        will be added and the stem with the highest weight for each tenders
        will be returned as the candidate tag. One thing to node, if there are
        few words in a tender that pointed to the highest stem
        (e.g., orig_word: [manager, management, managing] -> stem: [manage]),
        all these words will be returned.

        Returns
        -------
        A dataframe with the shape of n*4. PKs are [items, key_orig]
        Columns: 'items': matching with each tenders project.
                 'key': extracted stem with the highest weight.
                 'key_orig': original word corresponding to the key.
                 'value': total weight for the final stem
        '''

        reg_rule = r'\((.*?)\)'
        input_df[target_col] = input_df[target_col].astype(str)

        # Extract and reformat term-weight set
        tmp_df = input_df[target_col].str.extractall(reg_rule).reset_index().reset_index()
        split_result = tmp_df[0].str.split(',', expand=True).rename(columns={0: 'key',
                                                                             1: 'value'}).reset_index()

        merge_df = tmp_df.merge(split_result, on='index').drop('index', axis=1).rename(columns={'level_0': 'items'})
        del tmp_df, split_result

        merge_df['key'] = merge_df['key'].map(self.__split_words)
        mapping_df = merge_df.explode('key')[['items', 'key', 'value']]
        mapping_df['key_orig'] = mapping_df['key']
        # mapping_df['key'] = mapping_df['key'].map(nltk.PorterStemmer().stem)

        # Compute weight according to each word and ordering
        mapping_df['value'] = mapping_df['value'].astype(float)
        sum_df = mapping_df.groupby(['items', 'key', 'key_orig'])['value'].sum().reset_index().sort_values(
            ['items', 'value'], ascending=False)

        # Sampling top key
        key_df = sum_df.groupby(['items']).head(1)[['items', 'key']]
        merge_df = sum_df.merge(key_df, on=['items', 'key'])
        return merge_df

    def get_label_by_iteration(self, input_df: pd.DataFrame, pk: str, text_col: str, iterations=5) -> pd.DataFrame:
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
        pd.DataFrame, original dataframe appending with key columns:
                                [key_0,	key_1, key_2, key_3, key_4]
        '''

        df = input_df.copy()
        assert text_col in df.columns, f'Missing column names "{text_col}".'

        df[text_col] = df[text_col].map(lambda x: self.__convert_word_type(x))

        # Remove pure numbers, e.g., 2014, 20,000
        df[text_col] = df[text_col].map(lambda x: re.sub(r'\s*(\.:,|\d+)\s*', '', x))
        df = df.reset_index(drop=True).reset_index()

        for i in range(iterations):
            print(f'Start iteration {i}')

            # Get keywords in one around
            df['raw_result'] = df.apply(self.__get_tags, axis=1)

            # Aggregate keywords
            merge_df = self.__agg_tags(df, 'raw_result')
            key_df = merge_df.groupby(['items', 'key'])['key_orig'].apply(lambda x: list(set(x))).reset_index()

            first_df = df[['index', 'text']].merge(key_df, left_on='index', right_on='items', how='left')

            # Generating new text
            df = df.drop('text', axis=1)
            first_df = first_df[first_df['key_orig'].notna()].apply(self.__remove_keywords, axis=1).rename(
                columns={'key': f'key_{i}'}).drop(['items', 'key_orig'], axis=1)
            df = df.merge(first_df, on='index', how='left')

            assert len(df) == len(input_df), \
                f'Tenders which {df} in {set(input_df[pk].unique().tolist()) - set(df[pk].unique().tolist())} lost'

            print(f'End iteration {i}')
        df = df.replace('[none_tag]', np.nan)
        return df


if __name__ == '__main__':
    input_df_1 = pd.read_csv('../dataset/tenders/relevant.csv')
    input_df_1['text'] = input_df_1['Description'] + '.' + input_df_1['Title']
    input_df_1['ID'] = 'TENDERS.' + input_df_1['ATM ID']
    input_df_1 = input_df_1[['ID', 'text', 'Description', 'Title', 'Category']]
    input_df_2 = pd.read_csv('../dataset/tenders/Gos.csv')
    input_df_2['Category'] = input_df_2['Primary Category'] + '.' + input_df_2['Secondary Category']
    input_df_2['text'] = input_df_2['Description'] + '.' + input_df_2['Title'] + '.' + input_df_2['Category']
    input_df_2['ID'] = 'GOS.' + input_df_2['GO ID']
    input_df_2 = input_df_2[['ID', 'text', 'Description', 'Title', 'Category']]
    input_df = input_df_1.append(input_df_2)
    # input_df = pd.concat([input_df.iloc[542],input_df.iloc[546], input_df.iloc[1411], input_df.iloc[1423], input_df.iloc[1822]], axis=1).T
    ke = KeyExtractor()
    re_df = ke.get_label_by_iteration(input_df, 'ID', 'text')
    re_df.to_csv('remove_num_tenders.csv', index=0, encoding='utf-8_sig')
