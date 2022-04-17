def split_tag(row):
    re = []
    for i in row:
        re.append(i.split('<weight>'))
    return re


def convert_to_num(value):
    return int(value.replace('"', '')[:-1]) / 100


def data_clean(input_df, region, pk, ref_col='_id'):
    input_df[pk] = region + '_' + input_df[ref_col]
    rename_dict = {}
    for col in input_df.columns:
        new_col = col.lower()
        if 'tag' not in col:
            rename_dict[col] = new_col
    info_df = input_df.copy()
    info_df.rename(columns=rename_dict, inplace=True)

    input_df['pt'] = input_df['ProjectTags'].str.split('<bk>')
    input_df['st'] = input_df['staffTags'].str.split('<bk>')

    tag_df = input_df[[pk, 'pt', 'st']].copy()
    tag_df.loc[tag_df['pt'].notna(), 'pt'] = tag_df[tag_df['pt'].notna()]['pt'].map(split_tag)
    tag_df.loc[tag_df['st'].notna(), 'st'] = tag_df[tag_df['st'].notna()]['st'].map(split_tag)

    tag_df = tag_df.melt(id_vars=pk)
    tag_df = tag_df.explode('value')
    tag_df = tag_df.dropna()
    tag_df['tag'] = tag_df['value'].map(lambda x: x[0])
    tag_df['weight'] = tag_df['value'].map(lambda x: x[1])
    tag_df = tag_df.drop('value', axis=1).rename(columns={'variable': 'tag_type'})
    tag_df['tag_type'] = tag_df['tag_type'].map(lambda x: 'project_key' if x == 'pt' else 'staff_key')
    tag_df['tag'] = tag_df['tag'].str.lower()
    tag_df['weight'] = tag_df['weight'].map(convert_to_num)
    tag_df = tag_df.drop_duplicates()

    return info_df, tag_df
