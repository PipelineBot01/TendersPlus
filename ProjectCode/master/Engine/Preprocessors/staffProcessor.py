import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder

from ProjectCode.dev.Engine.Preprocessors.BaseProcessors import TextProcessor


class StaffProcessor():
    """
        the processor of stuff data
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

        def tagsFromData(df: pd.DataFrame, tagsType: str) -> pd.DataFrame:
            data = np.array(df)
            data_ = np.apply_along_axis(dataPreprocess, 1, data)
            tags_list = []
            weight_list = []
            staff_id_list = []
            tagsType_list = []
            for i in range(data_.shape[0]):
                for key in data_[i].keys():
                    tags_list.append(key)
                    weight_list.append(data_[i][key][0])
                    staff_id_list.append(data_[i][key][1])
                    tagsType_list.append(tagsType)
            new_df = pd.DataFrame({'Tags': tags_list, 'Weight': weight_list, 'Staff ID': staff_id_list,
                                   'tagsType': tagsType_list})
            return new_df

        def dataPreprocess(data: np.ndarray) -> dict:
            attributes = tp.textPreprocess(data[1])
            data_dict = {}
            for key in attributes.keys():
                weight = attributes[key]
                data_list = [weight, data[0]]
                data_dict[key] = data_list
            return data_dict

        col_name = self.data.columns.tolist()
        col_name.insert(0, 'Staff ID')
        self.data = self.data.reindex(columns=col_name)
        self.data['Staff ID'] = [self.data.loc[i, 'University'] + str("{:0>5d}".format(i)) for i in
                                 range(len(self.data.index))]

        df_1 = self.data.loc[:,
               ['Staff ID', 'Name', 'Email', 'OtherEmails', 'University', 'Colleges', 'Title', 'Profile']]
        df_2 = self.data.loc[:, ['Staff ID', 'StaffTags']]
        df_2['StaffTags'][df_2['StaffTags'].isnull()] = ''
        df_3 = self.data.loc[:, ['Staff ID', 'ProjectTags']]
        df_3['ProjectTags'][df_3['ProjectTags'].isnull()] = ''

        item_split_punctuation = r"<bk>"
        key_value_punctuation = r"<weight>"
        tp = TextProcessor(item_split_punctuation, key_value_punctuation)

        staffTags = tagsFromData(df_2, 'StaffTags')
        projectTags = tagsFromData(df_3, 'ProjectTags')

        Tags = staffTags.append(projectTags, ignore_index=True)
        self.infoData = df_1.set_index('Staff ID')
        self.featuresData = Tags.set_index('Tags')

    def transform(self) -> pd.DataFrame:
        """

        :return: dataframe of stuff's id, stuff's features, features' importance
        """

    def save(self):
        """
        save the data after transforming to a better structure
        :return:
        """
        self.infoData.to_csv('tendersplus/ProjectCode/master/Engine/assets/PreprocessResult/staffsInfo.csv')
        self.featuresData.to_csv('tendersplus/ProjectCode/master/Engine/assets/PreprocessResult/staffsTags.csv')

pwd = os.path.normpath(os.path.dirname(__file__)).split('tendersplus')[0]
os.chdir(pwd)
staffsProcessor = StaffProcessor('tendersplus/ProjectCode/master/Engine/assets/ScraperResult/ScraperResult_UC.csv')
staffsProcessor.dataProcess()
staffsProcessor.save()
