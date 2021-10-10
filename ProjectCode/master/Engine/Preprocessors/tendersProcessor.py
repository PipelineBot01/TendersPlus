import os

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

from ProjectCode.dev.Engine.Preprocessors.BaseProcessors import TextProcessor


class TendersProcessor():
    """
        the processor of tenders data
    """

    def __init__(self, path):
        self.features = {}
        self.data = pd.read_csv(path)
        self.infoData = None
        self.featuresData = None

    def featuresDetect(self):
        """

        :return:
        """

    def dataProcess(self):
        """
        do data preprocess to better data frame
        :return:
        """

        def attributesFromData(df: pd.DataFrame) -> list:
            data = np.array(df)
            data_ = np.apply_along_axis(dataPreprocess, 1, data)
            return data_.tolist()

        def dataPreprocess(data: np.ndarray) -> dict:
            attributes = tp.textPreprocess(data[0])
            return attributes

        df_1 = self.data.loc[:, ['Name', 'ID']]
        df_1 = df_1.rename(columns={'Name': 'Name', 'ID': 'ATM ID'})
        df_2 = self.data.loc[:, ['attributes']]

        item_split_punctuation = r"', '"
        key_value_punctuation = r"': '"
        tp = TextProcessor(item_split_punctuation, key_value_punctuation)
        data_list = [attribute for attribute in attributesFromData(df_2)]
        new_df_2 = pd.DataFrame(data_list)
        new_df_2_1 = new_df_2.filter(regex=r"[^Description]")
        new_df_2_2 = new_df_2.filter(regex=r"ATM ID|Description|Category")
        self.infoData = df_1.merge(new_df_2_1, how='inner', on='ATM ID').set_index('ATM ID')
        self.featuresData = df_1.merge(new_df_2_2, how='inner', on='ATM ID').set_index('ATM ID')

    def transform(self) -> pd.DataFrame:
        """
        :return: dataframe of tender's id, tender's features, features' importance
        """

    def save(self):
        """
        save the data after transforming to a better structure
        :return:
        """
        self.infoData.to_csv('tendersplus/ProjectCode/master/Engine/assets/PreprocessResult/tendersInfo.csv')
        self.featuresData.to_csv('tendersplus/ProjectCode/master/Engine/assets/PreprocessResult/tendersFeatures.csv')


# run example
pwd = os.path.normpath(os.path.dirname(__file__)).split('tendersplus')[0]
os.chdir(pwd)
tendersProcessor = TendersProcessor('tendersplus/ProjectCode/dev/Engine/Scraper/Tenders/results/tendersInfo.csv')
tendersProcessor.dataProcess()
tendersProcessor.save()
