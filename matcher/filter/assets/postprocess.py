import pandas as pd
from conf.file_path import RESEARCHER_ACTION_PATH


class PostProcess:
    def __init__(self,
                 user_action_path=RESEARCHER_ACTION_PATH):
        self.___action_df = pd.read_csv(user_action_path)

    def __get_popular_tenders(self):
        
    def process_data(self, tenders_df):
