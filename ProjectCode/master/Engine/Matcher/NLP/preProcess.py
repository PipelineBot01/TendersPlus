import pandas as pd
def preprocess(path):
    review=pd.read_csv(path)
    bio=review[pd.notnull(review.BioText)].BioText
    interests = review[pd.notnull(review.Interests)].Interests
    review=pd.DataFrame({'BioText':bio,'label1':None, 'Interests':interests,'label2':None})
    def pre(rows):
        if pd.notnull(rows.BioText):
            tempB=rows.BioText
            i = 1
            while 50 * i < len(tempB):
                tempB=tempB[:50 * i]+tempB[50 * i:].replace(' ','\n',1)
                # tempB.insert(50 * i, '\n')
                i += 1
            rows.BioText = tempB
        if pd.notnull(rows.Interests):
            tempI= rows.Interests
            j = 1
            while 50 * j < len(tempI):
                tempI = tempI[:50 *j] + tempI[50 *j:].replace(' ', '\n', 1)
                j+=1
            rows.Interests = tempI
        return rows
    review=review.apply(pre,axis=1)
    review.to_csv('textSample.csv')
path= '../../Scraper/Staffs/tempResult/oldPage/ScraperResult.csv'
preprocess(path)