import datetime
import re

import numpy as np
import pandas as pd
from conf.file_path import TENDERS_RELEVANT_PATH


def extract_award(item: str) -> str:
    if type(item) == type(np.nan):
        return item
    item = item.lower().replace(',', '')
    if 'from' in item:
        re_rule = 'From\$(\d+)to\$(\d+)'
        result = re.findall(re_rule, item)
        return '-'.join(str(int(i)) for i in result[0])
    return str(re.findall(r'\$(\d+)', item)[0])


def extract_time(row: str) -> str:
    result = re.findall('(\d+-[a-zA-Z]+-\d+)', row)
    return result[0]


def convert_dtype(input_df: pd.DataFrame):
    for col in input_df.columns:
        if '_date' in col:
            input_df[col] = pd.to_datetime(input_df[col], errors='coerce').dt.normalize()
            input_df[col].fillna('on_going', inplace=True)
    return input_df


def data_clean(input_df: pd.DataFrame, overwrite=False) -> pd.DataFrame:
    input_df = input_df[(input_df['GO ID'].notna()) & (input_df['GO ID'] != '') & (input_df['GO ID'] != 'None')]
    input_df.loc[:, 'id'] = 'Grants' + input_df['GO ID']
    input_df = input_df[['id',
                         'Agency',
                         'Publish Date',
                         'Close Date & Time',
                         'Title',
                         'Description',
                         'Eligibility',
                         'Primary Category',
                         'Secondary Category',
                         'Total Amount Available (AUD)',
                         'Location', 'Selection Process', 'GO ID'
                         ]].rename(columns={'Agency': 'agency',
                                            'Publish Date': 'open_date',
                                            'Close Date & Time': 'close_date',
                                            'Title': 'title',
                                            'Description': 'desc', 'Eligibility': 'elig',
                                            'Primary Category': 'category',
                                            'Secondary Category': 'sub_category',
                                            'Total Amount Available (AUD)': 'award',
                                            'Location': 'loc',
                                            'Selection Process': 'sp',
                                            'GO ID': 'go_id'})

    input_df.loc[input_df['close_date'] == 'Ongoing', 'is_on'] = 1
    input_df.loc[input_df['is_on'] != 1, 'close_date'] = input_df[input_df['is_on'] != 1]['close_date'].map(
        lambda x: extract_time(x))

    input_df['open_date'] = pd.to_datetime(input_df['open_date']).dt.normalize()
    input_df['close_date'] = pd.to_datetime(input_df['close_date'], errors='coerce').dt.normalize()
    input_df.loc[input_df['close_date'] >= datetime.datetime.now(), 'is_on'] = 1
    input_df['is_on'].fillna(0, inplace=True)

    if overwrite:
        input_df = input_df.append(pd.read_csv(TENDERS_RELEVANT_PATH))

    input_df['text'] = input_df['title'] + '.' + input_df['desc']
    return input_df