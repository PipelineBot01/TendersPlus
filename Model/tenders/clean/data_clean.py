import re
import time
import numpy as np
import pandas as pd



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


def update_opened_data(path):
    input_df = pd.read_csv(path)['id', 'title', 'open_date', 'close_date', 'url', 'tags', 'divisions']
    input_df = input_df[input_df['is_on'] == 1]
    save = []
    for i in input_df.columns:
        if 'key' in i:
            save.append(i)

    def reformat_key(row):
        row = row[save].dropna()
        return ' '.join(row[i] for i in row.index)

    input_df['tags'] = input_df.apply(lambda x: reformat_key(x), axis=1)
    input_df['division'] = 'test'
    return input_df
