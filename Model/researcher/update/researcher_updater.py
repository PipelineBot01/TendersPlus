import pandas as pd

class ResearcherUpdater:
    def __init__(self, pk: str):
        self.pk = pk
        self.raw_data_df = self.mongx.read_df('raw_grants_opened')
        self.raw_data_df['_id'] = self.raw_data_df['_id'].astype(str)
        self.raw_data_df['id'] = 'Grants' + self.raw_data_df['_id']
