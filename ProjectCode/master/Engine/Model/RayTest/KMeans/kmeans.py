import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
def cosine_similarity(x, y, norm=False):
    assert len(x) == len(y), "len(x) != len(y)"
    if len(x) == 1:
        return 1
    zero_list = [0] * len(x)
    if (x == zero_list).all() or (y == zero_list).all():
        return float(1) if x == y else float(0)

    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

    return 0.5 * cos + 0.5 if norm else cos

def kmeans():
    inputDate=np.load('../../../assets/Doc2vecResult/tenders_docvecs.npy',allow_pickle=True)
    vector=list(inputDate.item().values())
    input_df=pd.DataFrame(columns=[i for i in range(len(vector[0]))])
    for i in vector:
        tempDict={}
        for j in range(len(vector[0])):
            tempDict[j]=i[j]
        # print(tempDict)
        input_df=input_df.append(tempDict,ignore_index=True)
    # print(input_df)
    # clus = KMeans(n_clusters=19).fit(input_df)
    # centriods = clus.cluster_centers_
    # clusters = clus.labels_
    # dic={'clus':[],'description':[]}
    # for i in range(len(vector)):
    #     for k,v in inputDate.item().items():
    #         if (v==vector[i]).all():
    #             dic['clus'].append(clusters[i])
    #             dic['description'].append(k)
    #             break
    # pd.DataFrame.from_dict(dic).to_csv('cluster_result.csv',index=False)
    # return
    errors=[]
    for i in range(len(input_df)):
        error = []
        for time in range(1):
            clus=KMeans(n_clusters=i+1).fit(input_df)
            centriods=clus.cluster_centers_
            clusters=clus.labels_
            for c in range(i+1):
                temp = 0
                for index in range(len(clusters)):
                    if clusters[index]==c:
                        temp+=cosine_similarity(input_df.iloc[index],centriods[c]) #(sum((input_df.iloc[index]-centriods[c])**2))**(1/2)
                error.append(temp/list(clusters).count(c))
        errors.append(sum(error)/1)
        print(errors)
    plt.plot([i for i in range(len(input_df))], errors)
    plt.xlabel("cluster number")
    plt.ylabel("error")
    plt.show()
kmeans()