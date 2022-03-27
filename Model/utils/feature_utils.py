from nltk.corpus import stopwords

from conf.features import PROJECT_STOP_WORDS

STOP_WORDS = stopwords.words('english')


def filter_words(pos_tagged, lemmatizer):
    '''

    Parameters
    ----------
    pos_tagged
    lemmatizer

    Returns
    -------

    '''
    words = []
    noun = list(filter(
        lambda x: x[0] not in STOP_WORDS and (x[1].startswith('NN') or x[1].startswith('JJ')),
        pos_tagged))
    for word, pos in noun:
        if pos.startswith('NN'):
            word = lemmatizer.lemmatize(word, pos='n')
        elif pos.startswith('JJ'):
            word = lemmatizer.lemmatize(word, pos='a')
        if word not in PROJECT_STOP_WORDS:
            words.append(word)
    return words
