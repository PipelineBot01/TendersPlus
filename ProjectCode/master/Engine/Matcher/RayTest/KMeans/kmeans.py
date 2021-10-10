import numpy
import pandas as pd
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
def kmeans():
    inputDate=numpy.load('../../../assets/Doc2vecResult/tenders_docvecs.npy',allow_pickle=True)
    vector=list(inputDate.item().values())
    input_df=pd.DataFrame(columns=[i for i in range(len(vector[0]))])
    for i in vector:
        tempDict={}
        for j in range(len(vector[0])):
            tempDict[j]=i[j]
        # print(tempDict)
        input_df=input_df.append(tempDict,ignore_index=True)
    # print(input_df)
    errors=[]
    for i in range(len(input_df)):
        error = []
        for time in range(20):
            clus=KMeans(n_clusters=i+1).fit(input_df)
            centriods=clus.cluster_centers_
            clusters=clus.labels_
            for c in range(i+1):
                temp = 0
                for index in range(len(clusters)):
                    if clusters[index]==c:
                        temp+=(sum((input_df.iloc[index]-centriods[c])**2))**(1/2)
                error.append(temp/list(clusters).count(c))
        errors.append(sum(error)/20)
    plt.plot([i for i in range(len(input_df))], errors)
    plt.xlabel("cluster number")
    plt.ylabel("error")
    plt.show()
kmeans()