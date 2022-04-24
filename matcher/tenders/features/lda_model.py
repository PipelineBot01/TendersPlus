import gensim

from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk import pos_tag

import numpy as np
import pandas as pd
from gensim.test.utils import datapath

from conf.features import NUM_TOPICS
from conf.file_path import MODEL_FILE
from utils.feature_utils import filter_words


class LDAModel:
    def __init__(self, df, first=True, model_file=MODEL_FILE):
        '''

        Parameters
        ----------
        df: pd.DataFrame, input dataframe

        this function will do initiation of the lda model

        Returns
        -------
        '''

        self.relevant_tenders = df
        self.topic_word_dict = {}
        self.word_list = []
        self.dictionary = None
        self.corpus = None
        self.model_file = None
        self.first = first
        self.lda = None

    def build_lda_model(self):
        self.relevant_tenders.loc[:, 'ProcessedText'] = self.relevant_tenders.apply(self.document_process, axis=1)
        self.dictionary = gensim.corpora.Dictionary(self.word_list)
        self.dictionary.filter_extremes(no_above=0.5)
        self.dictionary.compactify()

        self.corpus = [self.dictionary.doc2bow(words) for words in self.word_list]
        print(self.word_list)
        self.lda = gensim.models.ldamodel.LdaModel(corpus=self.corpus, id2word=self.dictionary, num_topics=NUM_TOPICS,
                                                   iterations=500)

        for topic_id in range(NUM_TOPICS):
            templist = []
            term_distribute_all = self.lda.get_topic_terms(topicid=topic_id, topn=20)
            term_distribute = term_distribute_all[:]
            term_distribute = np.array(term_distribute)
            term_id = term_distribute[:, 0].astype(np.int)
            for t in term_id:
                templist.append(self.dictionary.id2token[t])
            self.topic_word_dict[topic_id] = templist

    def document_process(self, relevant_tenders):
        '''
        Parameters:
        -------
        relevant_tenders: dataframe that will do process
        this function will do some document process before build the LDA model.
        strategies:
        1.  tokenize the text that will be processed
        2.  filter words that only is noun and adjective and lemmatize the words
        3.  the global word dictionary will append these words.

        Returns
        -------
        List[Tuple[str, float]], list of words that only is noun and adjective.
        '''
        text = relevant_tenders['text']
        token = word_tokenize(str(text).lower())
        lemmatizer = WordNetLemmatizer()
        pos_tagged = pos_tag(token)
        words = filter_words(pos_tagged, lemmatizer)

        self.word_list.append(words)
        return words

    def extract_keyword(self, data):
        templist2 = []
        token = word_tokenize(str(data).lower())
        lemmatizer = WordNetLemmatizer()
        pos_tagged = pos_tag(token)
        words = filter_words(pos_tagged, lemmatizer)

        doc_topics = self.get_doc_topic(data)

        for tp in doc_topics:
            temp_word = self.topic_word_dict[tp[0]]
            templist2 += temp_word
        doc_word_dict = templist2
        keyword = []
        for word in words:
            if word in doc_word_dict:
                keyword.append(word)
        return set(keyword)

    def get_doc_topic(self, data):
        token = word_tokenize(str(data).lower())
        lemmatizer = WordNetLemmatizer()
        pos_tagged = pos_tag(token)

        words = filter_words(pos_tagged, lemmatizer)

        doc_bow = self.dictionary.doc2bow(words)
        doc_topics = self.lda.get_document_topics(doc_bow)
        return doc_topics

    def load_lda_model(self):
        lda_model = gensim.models.ldamodel.LdaModel.load(self.model_file)
        return lda_model

    def add_lda_result_to_data(self):
        self.relevant_tenders['keywords'] = self.relevant_tenders.apply(self.extract_keyword, axis=1)
        self.relevant_tenders['topics'] = self.relevant_tenders.apply(self.get_doc_topic, axis=1)

    def get_tenders_topic(self):
        self.add_lda_result_to_data()
        return self.relevant_tenders[['id', 'topics']]

    def get_key_topic(self, num_words):
        topics = self.lda.show_topics(num_topics=NUM_TOPICS, num_words=num_words)
        topic_dic = dict()
        for topic in topics:
            temp = []
            topic_id = topic[0]
            topic_words = topic[1].split(' + ')
            for topic_word in topic_words:
                word = tuple(topic_word.replace('"', '').split('*'))
                temp.append(word)
            topic_dic[topic_id] = temp
        df = pd.DataFrame.from_dict(topic_dic, orient='index', columns=['keyword' + str(i) for i in range(num_words)])
        return df
