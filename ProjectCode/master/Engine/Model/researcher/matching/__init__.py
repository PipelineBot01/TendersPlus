import pandas as pd
from conf.division import RESEARCH_FIELDS
info=pd.read_csv('../assets/tag_category_map.csv')
re_dict = {}
for k, v in RESEARCH_FIELDS.items():
    re_dict[v['field']] = k
info.loc[~info['value'].isin(['OTHERS(IRRELEVANT)', 'OTHERS(RELEVANT)']), 'value'] = \
    info[~info['value'].isin(['OTHERS(IRRELEVANT)', 'OTHERS(RELEVANT)'])]['value'].map(lambda x: re_dict[x])
print(info['value'].unique())
# info.to_csv('../assets/new.csv', index=0)
# info=pd.read_csv('../assets/new.csv')
# info.loc[~info['value'].isin(['OTHERS(IRRELEVANT)', 'OTHERS(RELEVANT)']), 'value'] = \
#     info[~info['value'].isin(['OTHERS(IRRELEVANT)', 'OTHERS(RELEVANT)'])]['value'].map(lambda x: RESEARCH_FIELDS[x]['field'])
# info.to_csv('../assets/new_info.csv', index=0)
