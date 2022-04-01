import re
import datetime
import numpy as np
import pandas as pd
from conf.file_path import TENDERS_INFO_PATH, TENDERS_TAG_PATH, TENDERS_RELEVANT_PATH


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


def convert_dtype(input_df:pd.DataFrame):
    for col in input_df.columns:
        if '_date' in col:
            input_df[col] = pd.to_datetime(input_df[col], errors='coerce').dt.normalize()
            input_df[col].fillna('on_going', inplace=True)
    return input_df


def data_clean(input_df: pd.DataFrame, overwrite=False) -> pd.DataFrame:
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
                         'Total Amount Available (AUD)', 'GO ID',
                         'Location', 'Internal Reference ID', 'Selection Process',
                         'URL']].rename(columns={'Agency': 'agency',
                                                 'Publish Date': 'open_date',
                                                 'Close Date & Time': 'close_date',
                                                 'Title': 'title',
                                                 'Description': 'desc', 'Eligibility': 'elig',
                                                 'Primary Category': 'category',
                                                 'Secondary Category': 'sub_category',
                                                 'Total Amount Available (AUD)': 'award',
                                                 'Location': 'loc',
                                                 'URL': 'url',
                                                 'GO ID': 'go_id',
                                                 'Internal Reference ID': 'irf_id',
                                                 'Selection Process': 'sp'})
    input_df.loc[input_df['close_date'] == 'Ongoing', 'is_on'] = 1
    input_df.loc[input_df['is_on'] != 1, 'close_date'] = input_df[input_df['is_on'] != 1]['close_date'].map(
        lambda x: extract_time(x))

    input_df['open_date'] = pd.to_datetime(input_df['open_date']).dt.normalize()
    input_df['close_date'] = pd.to_datetime(input_df['close_date'], errors='coerce').dt.normalize()
    input_df.loc[input_df['close_date'] >= datetime.datetime.now(), 'is_on'] = 1
    input_df['is_on'].fillna(0, inplace=True)

    if overwrite:
        input_df = input_df.append(pd.read_csv(TENDERS_RELEVANT_PATH))

    input_df['text'] = input_df['title'] + '.' +input_df['desc']
    return input_df


def update_opened_data(info_path=TENDERS_INFO_PATH, tag_path=TENDERS_TAG_PATH):
    info_df = pd.read_csv(info_path)
    info_df = info_df[info_df['is_on'] == 1][['id', 'title',
                                  'category', 'desc',
                                  'open_date', 'close_date',
                                  'url', 'loc', 'go_id', 'irf_id', 'sp']]

    tag_df = pd.read_csv(tag_path)

    def reformat_key(row):
        row = row.dropna()
        return ' '.join(row[i] for i in row.index[1:])

    tag_df['tags'] = tag_df.apply(lambda x: reformat_key(x), axis=1)
    info_df = info_df.merge(tag_df[['id', 'tags']], on= 'id')
    info_df['division'] = 'test'
    info_df = convert_dtype(info_df)
    return info_df

if __name__ =='__main__':
    from db.mongodb import MongoConx
    mgx = MongoConx('tenders')
    raw_df = mgx.read_df('raw_grants_all')
    result = data_clean(raw_df, overwrite=True)
    result.to_csv(TENDERS_INFO_PATH)
    new_open_info = update_opened_data()
    mgx.write_df(new_open_info, 'clean_grants_opened', overwrite=True)
