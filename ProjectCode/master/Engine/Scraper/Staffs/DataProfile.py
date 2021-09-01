import pandas as pd
import matplotlib.pyplot as plt
import nltk
import numpy as np
review = pd.read_csv('../../assets/ScraperResult/ScraperResult_UC.csv')

def bar_number_h(category,value,value2):
    for index in range(len(category)):
        rect=category[index]
        if type(value[index])==type(1): plt.text(value2[index], rect.get_y()+rect.get_height()/2, '%d' %value[index], ha='left', va='center')
        else: plt.text(value2[index], rect.get_y()+rect.get_height()/2, '%0.2f' %value[index], ha='left', va='center')

def overview(review):
    review=review.dropna(axis=0,how='any',subset=['ProjectTags'])
    re=0
    for i in review.ProjectTags:
        data = i.split('<bk>')
        re+=len(data)
    review = review.dropna(axis=0, how='any', subset=['Colleges'])
    review=review.Colleges
    dic={}
    for i in review:
        v=1
        if i in dic.keys():
            v=dic[i]+1
        dic.update({i:v})

    dic=sorted(dic.items(),key=lambda x:x[1],reverse=True)
    Y_axis = np.arange(10)
    x1 = [i[1] for i in dic[:10]][::-1]
    print(x1)
    # plt.figure(figsize=(10, 10))
    proportion = plt.barh(Y_axis,x1, 0.5, label='number', color='deepskyblue', alpha=1)
    bar_number_h(proportion, x1, x1)
    # plt.ylim(0, 1.0)
    plt.yticks(Y_axis, [i[0] for i in dic[:10]][::-1])
    plt.ylabel("Institution")
    plt.xlabel("Number of staffs")
    # plt.legend()
    plt.show()
    print(dic)
overview(review)
def getstaffTags(review):
    staffTags=review.dropna(subset=['ProjectTags'])
    countstaff={}
    for item in staffTags.ProjectTags:
        tags=item.split('<bk>')
        for tag in tags:
            tag=tag.split('<weight>')
            tag[0]=tag[0].lower()
            tag[0]=nltk.stem.WordNetLemmatizer().lemmatize(tag[0])
            if tag[0] in countstaff.keys():
               v=countstaff.get(tag[0])+1
               countstaff.update({tag[0]:v})
            else: countstaff.update({tag[0]:1})
    countstaff=sorted(countstaff.items(),key=lambda x:x[1],reverse=True)
    tag_items=[i[0] for i in countstaff[0:10]][::-1]
    item_count=[i[1] for i in countstaff[0:10]][::-1]

    Y_axis = np.arange(10)

    proportion = plt.barh(Y_axis, item_count, 0.5, label='number', color='orange', alpha=1)
    bar_number_h(proportion, item_count, item_count)
    plt.yticks(Y_axis, tag_items)
    plt.ylabel("Project tag")
    plt.xlabel("Number of tag")
    plt.show()
    return tag_items,item_count

def getPublicationTags(review):
    staffTags=review.dropna(subset=['ProjectTags'])
    countstaff={}
    for item in staffTags.ProjectTags:
        tags=item.split('<bk>')
        for tag in tags:
            tag=tag.split('<weight>')
            tag[0]=tag[0].lower()
            tag[0]=nltk.stem.WordNetLemmatizer().lemmatize(tag[0])
            if tag[0] in countstaff.keys():
               v=countstaff.get(tag[0])+1
               countstaff.update({tag[0]:v})
            else: countstaff.update({tag[0]:1})
    return countstaff
    countstaff=sorted(countstaff.items(),key=lambda x:x[1],reverse=True)
    tag_items=[i[0] for i in countstaff[0:20]][::-1]
    item_count=[i[1] for i in countstaff[0:20]][::-1]
    return tag_items,item_count
def getItem(tag):
    tag = tag.split('<weight>')[0]
    tag = tag.lower()
    tag = nltk.stem.WordNetLemmatizer().lemmatize(tag)
    return tag

def get_staff_to_Pub(review):
    review=review.loc[:, ['Name','Colleges','StaffTags', 'ProjectTags']]
    tags = review.dropna()
    staffDic={}
    collegeDic={}
    for index in tags.index:
        count=0
        stags=tags.loc[index].values[2].split('<bk>')
        ptags=tags.loc[index].values[3].split('<bk>')
        ptagList=[]
        for ptag in ptags:
            ptag=getItem(ptag)
            ptagList.append(ptag)
        for stag in stags:
            stag=getItem(stag)
            if stag in ptagList:count+=1
        staffDic.update({tags.loc[index].values[0]:round(count/len(stags),2)})

        if tags.loc[index].values[1] in collegeDic.keys():
            v=collegeDic[tags.loc[index].values[1]]
            v.append(round(count/len(stags),2))
        else: collegeDic.update({tags.loc[index].values[1]:[round(count/len(stags),2)]})
    staffDic2=staffDic
    staffDic = {}
    collegeDic = {}
    for index in tags.index:
        count=0
        stags=tags.loc[index].values[3].split('<bk>')
        ptags=tags.loc[index].values[2].split('<bk>')
        ptagList=[]
        for ptag in ptags:
            ptag=getItem(ptag)
            ptagList.append(ptag)
        for stag in stags:
            stag=getItem(stag)
            if stag in ptagList:count+=1
        staffDic.update({tags.loc[index].values[0]:round(count/len(stags),2)})

        if tags.loc[index].values[1] in collegeDic.keys():
            v=collegeDic[tags.loc[index].values[1]]
            v.append(round(count/len(stags),2))
        else: collegeDic.update({tags.loc[index].values[1]:[round(count/len(stags),2)]})
    def getDistrubution(staffDic):
        cdict_org = {}
        cdict={}
        for i in range(0, 100):
            cdict_org.update({i / 100: 0})
        for i in range(0, 10):
            cdict.update({i / 10: 0})
        for k, v in staffDic.items():
            count = 0
            if round(v,1) in cdict.keys():
                count = cdict[round(v,1)] + 1
            cdict.update({round(v,1): count})
            count = 0
            if v in cdict_org.keys():
                count = cdict_org[v] + 1
            cdict_org.update({v: count})

        cdict_org = sorted(cdict_org.items(), key=lambda x: x[0])
        cdict = sorted(cdict.items(), key=lambda x: x[0])


        maxi = max(i[1] for i in cdict)
        maxi_org=max(i[1] for i in cdict_org)

        x_org = [i[0] for i in cdict_org]
        y_org = [i[1] for i in cdict_org]

        x = [i[0] for i in cdict]
        y=[i[1]/maxi*maxi_org for i in cdict]
        from scipy import interpolate
        xnew = np.arange(0, 1, 0.001)
        func = interpolate.interp1d(x, y, kind='cubic')
        ynew = func(xnew)

        plt.plot(x_org,y_org,LineWidth=2,label='original', color='navy', alpha=0.3)
        plt.plot(xnew, ynew,LineWidth=2, label='binning 0.1', color='red', alpha=0.3)

        plt.ylabel("count")
        plt.xlabel("proportion")
        plt.title('Count of proportion for publication tags in staff tags  ')
        plt.legend(loc='upper left',numpoints = 1 )
        plt.show()


    def drawScatter(staffDic,staffDic2):
        college=staffDic.keys()
        x1 = [i for i in staffDic.values()]
        x2 = [i for i in staffDic2.values()]
        Y_axis = np.arange(len(college))
        point = plt.scatter(Y_axis, x2, 6, label='sta_to_pub', color='deepskyblue', alpha=0.5)
        point = plt.scatter(Y_axis,x1,6, label='pub_to_sta', color='salmon', alpha=0.5)

        plt.ylim(0,1)
        plt.ylabel("percentage")
        plt.xlabel("staff index")
        plt.legend()
        plt.show()

    def min_max(collegeDic):
        college=collegeDic.keys()
        x1 = [min(i[1]) for i in collegeDic.items()]
        x2 = [max(i[1]) for i in collegeDic.items()]
        avg=[round(sum(i)/len(i),2) for i in collegeDic.values()]

        median = [sorted(i)[len(i)//2] for i in collegeDic.values()]

        Y_axis = np.arange(len(college))

        plt.figure(figsize=(10, 10))
        proportion = plt.barh(Y_axis, x1, 0.6, label='min', color='grey', alpha=0.5)
        number = plt.barh(Y_axis, x2, 0.6, label='max', color='red', alpha=0.3)
        point=plt.scatter(avg,Y_axis, label='mean', color='darkred', alpha=1)
        point = plt.scatter(median, Y_axis, label='median', color='deeppink', alpha=1)
        import random
        random.randint()
        bar_number_h(proportion, x1, x1)
        bar_number_h(number, x2, x2)

        plt.yticks(Y_axis, Y_axis)
        plt.title('sta_to_pub by institution')
        plt.ylabel("institution index")
        plt.xlabel("percentage")
        plt.legend()
        plt.show()
        return

    def avgPro_Number(collegeDic,collegeCount):
        for k,v in collegeDic.items():
            collegeCount.update({k:len(v)})
            v=round(sum(v)/len(v),2)
            collegeDic.update({k:v})

        collegeCount = sorted(collegeCount.items(), key=lambda x: x[1], reverse=True)
        college=[i[0] for i in collegeCount]

        maxi=max(i[1] for i in collegeCount)
        collegeCount=[i[1] for i in collegeCount]
        normCount=[i / maxi  for i in collegeCount]

        collegeDic=[collegeDic[i] for i in college]

        x1 = collegeDic
        x2 = normCount

        Y_axis = np.arange(len(college))

        plt.figure(figsize=(10,10))
        proportion = plt.barh(Y_axis, x1, 0.6, label='AVG Proportion',color='grey', alpha=0.5)
        number = plt.barh(Y_axis, x2, 0.6, label='Number of staff',color='green', alpha=0.3)

        bar_number_h(proportion,x1,x1)
        bar_number_h(number,collegeCount,x2)

        plt.yticks(Y_axis, Y_axis)
        plt.title('pub_to_sta by institution')
        plt.ylabel("institution index")
        plt.xlabel("percentage")
        plt.legend()
        plt.show()

    drawScatter(staffDic,staffDic2)


def drawPlot(tag_items,item_count):
    fig, ax=plt.subplots()
    b = ax.barh(range(len(tag_items)), item_count, color='#6699CC')
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y()+rect.get_height()/2,'%d' %int(w), ha='left', va='center')
    ax.set_yticks(range(len(tag_items)))
    ax.set_yticklabels(tag_items)
    plt.xticks(())
    plt.show()

get_staff_to_Pub(review)
# overview(review)
# get_staff_to_Pub(review)