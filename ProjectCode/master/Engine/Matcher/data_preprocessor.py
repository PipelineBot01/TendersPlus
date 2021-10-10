"""
********** <[ STEP 2nd ]> **********

What to do:
- data_preprocessor will combine name, category and description as a document for each tender,
  it will tokenize each document, and lowercase, remove stopwords, remove digits, remove punctuation, lemmatize

Authors:
- Yuxuan Yang u7078049

"""

import nltk, os, pickle, pandas as pd, string, re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from Matcher.data_loader import load

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# remove the tenders if the description is not clear(words less than 20)
string_threshold = 40


def get_wordnet_pos(pos):
    if pos.startswith('J'):
        return 'a'
    elif pos.startswith('V'):
        return 'v'
    else:
        return 'n'


def doc_to_words(doc):
    """
    this process will turn each document or long string, into a list of words
    process:
    - lower case
    - remove punctuation
    - remove numbers
    - lemmatize

    """
    try:
        words = []
        tokens = nltk.word_tokenize(doc)
        if len(tokens) < string_threshold:
            return ''
        tokens = nltk.pos_tag(tokens)

        for (t, pos) in tokens:
            w = t.lower()
            w= w.strip()
            w = w.strip(string.punctuation)
            if w in stop_words:
                continue

            abbr_pos = get_wordnet_pos(pos)
            # if abbr_pos !='n':
            #     continue

            w = w.strip(string.digits)
            if w != '' and len(w) > 1:
                w = lemmatizer.lemmatize(w, pos=abbr_pos)
                words.append(w)
    except:
        return ''

    return words

def doc_to_words_2(doc):
    """
    this process will turn each document or long string, into a list of words
    process:
    - lower case
    - remove punctuation
    - remove numbers
    - lemmatize

    """
    try:
        words = []
        tokens = nltk.word_tokenize(doc)
        tokens = nltk.pos_tag(tokens)

        for (t, pos) in tokens:
            w = t.lower()
            w = w.strip()
            w = w.strip(string.punctuation)
            w = w.strip(string.digits)
            if w in stop_words:
                continue

            abbr_pos = get_wordnet_pos(pos)

            if w != '' and len(w) > 1:
                w = lemmatizer.lemmatize(w, pos=abbr_pos)
                words.append(w)
    except:
        return ''

    return words

if __name__ =="__main__":
    # ====== load history_tenders =========
    if (os.path.isfile('../Out/history_tenders_unprocessed')):
        with open('../Out/history_tenders_unprocessed', 'rb') as f:
            data = pickle.load(f)
    else:
        print("reload data from database")
        data = load()

    # ====== process history_tender =======
    data["Document"] = data['Title'] + '. ' + data['Category'] + '. ' + data['Description']
    pattern_1 = re.compile(r'http.*? ')
    pattern_2 = re.compile(r'www.*? ')
    data['Document'] = data['Document'].str.replace(pattern_1, '', regex=True)
    data['Document'] = data['Document'].str.replace(pattern_2, '', regex=True)
    data['Document'] = data['Document'].map(lambda x: doc_to_words(x))
    data = data.drop(data[data['Document'] == ''].index)
    print(data.shape)

    with open('../Out/history_tenders_processed', 'wb') as f:
        pickle.dump(data, f)
