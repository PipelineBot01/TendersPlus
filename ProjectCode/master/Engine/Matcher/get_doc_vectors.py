"""
********** <[ STEP 3rd ]> **********

What to do:
- use the processed data to train the doc2vec model,
  then we can this model to represent each tenders

Authors:
- Yuxuan Yang u7078049

"""

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import multiprocessing, os, pickle, pandas as pd


def fit_d2v(documents, vector_size=300):
    cores = multiprocessing.cpu_count()
    print('[fit_d2v]:: start training')

    #   dm=0,
    model = Doc2Vec(documents=documents, vector_size=vector_size, epochs=2000, workers=cores - 1,
                    dm_concat=0,
                    dm_mean=1,
                    dm=1,
                    alpha=0.001,
                    min_count=3,
                    hs=0,
                    dbow_words=1)
    model.save(f'../Out/doc2vec-{vector_size}.model')
    print('[fit_d2v]:: end training')
    return model


def get_d2v(filename):
    if (os.path.isfile(filename)):
        return Doc2Vec.load(filename)
    else:
        print('the file is not existed')
        return

def get_documents(filename):
    if (os.path.isfile(filename)):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
    else:
        print('the file is not existed')
        return

    data['TaggedDocument'] = data[['Document', 'ATM ID']].apply(lambda x: TaggedDocument(x['Document'], [x['ATM ID']]),
                                                                axis=1)
    return data['TaggedDocument']


if __name__ == '__main__':
    documents = list(get_documents('../Out/history_tenders_processed'))
    stat = []
    for i in documents:
        stat.append(len(i[0]))

    print(pd.DataFrame(stat).describe())
    fit_d2v(documents,vector_size=300)
