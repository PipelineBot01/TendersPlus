import re

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


class TextProcessor:
    """
    Class for carrying all the text pre-processing stuff throughout the project
    """

    def __init__(self, item_split_punctuation, key_value_punctuation):
        self.stopwords = stopwords.words('english')
        self.ps = PorterStemmer()
        self.item_split_punctuation = item_split_punctuation
        self.key_value_punctuation = key_value_punctuation

        # stemmer will be used for each unique word once
        self.stemmed = dict()

    def textPreprocess(self, text: str) -> dict:
        """
        preprocess the original data from website, make it as key-value pairs into a dict
        :param text: the text of description to extract attributes
        :return attributes:  the dict of the attributes from the descriptions
        """
        text = re.sub(r"^{'|'}$", '', text)
        text = re.sub(r'"', "'", text)
        if text == '':
            return dict()
        items = re.split(self.item_split_punctuation, text)
        attributes = dict()
        for i in items:
            pair = re.split(self.key_value_punctuation, i, 1)
            if len(pair) != 2:
                continue
            key = pair[0]
            value = pair[1]
            attributes[key] = value
        return attributes

    def process(self, text: str, allow_stopwords: bool = False) -> str:
        """
        Process the specified text,
        splitting by non-alphabetic symbols, casting to lower case,
        removing stopwords, HTML tags and stemming each word

        :param text: text to precess
        :param allow_stopwords: whether to remove stopwords
        :return: processed text
        """
        ret = []

        # split and cast to lower case
        text = re.sub(r'<[^>]+>', ' ', str(text))
        for word in re.split('[^a-zA-Z]', str(text).lower()):
            # remove non-alphabetic and stop words
            if (word.isalpha() and word not in self.stopwords) or allow_stopwords:
                if word not in self.stemmed:
                    self.stemmed[word] = self.ps.stem(word)
                # use stemmed version of word
                ret.append(self.stemmed[word])
        return ' '.join(ret)
