import re
import time

import numpy as np
import pandas as pd

from conf.file_path import TENDERS_INFO_PATH


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
    return result


def data_clean(input_df: pd.DataFrame) -> pd.DataFrame:
    input_df['id'] = 'Grants' + input_df['_id']
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
                         'URL']].rename(columns={'Agency': 'agency',
                                                 'Publish Date': 'open_date',
                                                 'Close Date & Time': 'close_date',
                                                 'Title': 'title',
                                                 'Description': 'desc', 'Eligibility': 'elig',
                                                 'Primary Category': 'category',
                                                 'Secondary Category': 'sub_category',
                                                 'Total Amount Available (AUD)': 'award',
                                                 'Location': 'loc',
                                                 'URL': 'url'})
    input_df.loc[input_df['close_date'] == 'Ongoing', 'is_on'] = 1
    input_df['is_on'].input_df(0, inplace=True)
    input_df.loc[input_df['is_on'] == 0, 'close_date'] = input_df[input_df['is_on'] == 0]['close_date'].map(
        lambda x: extract_time(x))

    input_df['open_date'] = pd.to_datetime(input_df['open_date']).dt.normalize()
    input_df['close_date'] = pd.to_datetime(input_df['close_date'], errors='coerce').dt.normalize()
    input_df.loc[input_df['close_date'] >= time.ctime(), 'is_on'] = 1
    input_df['is_on'].fillna(0, inplace=True)
    return input_df


def update_opened_data():
    all_df = pd.read_csv(TENDERS_INFO_PATH)['id', 'title', 'open_date', 'close_date', 'url', 'tags', 'divisions']
    return all_df
