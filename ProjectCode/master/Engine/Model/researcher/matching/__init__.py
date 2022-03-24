import pandas as pd
tmp = pd.read_csv('../assets/researcher_division.csv', encoding='utf-8_sig')
tmp.to_pickle('../assets/ researcher_division_pickle')