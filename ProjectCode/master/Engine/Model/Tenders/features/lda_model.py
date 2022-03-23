import gensim
import nltk
import numpy as np
import pandas as pd
from gensim.test.utils import datapath
from utils.match_utils import filter_words
from conf.file_path import TENDERS_INFO_PATH, MODEL_FILE, TENDERS_TOPIC_PATH


NUM_TOPICS = 22  # total topics that are set in lda model
NUM_SHOW_TERM = 20  # the number of words in the topic that want to be showed


class LDAModel:
    def __init__(self, df, first=True, model_file=MODEL_FILE):
        '''

        Parameters
        ----------
        df: pd.DataFrame, input dataframe

        this function will do initiation of the lda Model

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
        if not first:
            self.lda = self.loadLDAModel()
        if not self.first:
            self.model_file = datapath(model_file)

    def build_lda_model(self):
        self.relevant_tenders['ProcessedText'] = self.relevant_tenders.apply(self.document_process, axis=1)
        self.dictionary = gensim.corpora.Dictionary(self.word_list)
        self.dictionary.filter_extremes(no_above=0.5)
        self.dictionary.compactify()

        self.corpus = [self.dictionary.doc2bow(words) for words in self.word_list]

        self.lda = gensim.models.ldamodel.LdaModel(corpus=self.corpus, id2word=self.dictionary, num_topics=NUM_TOPICS,
                                                   iterations=500)

        # for topic in self.lda.print_topics(num_words=NUM_SHOW_TERM):
        #     print(topic)
        for topic_id in range(NUM_TOPICS):
            templist = []
            term_distribute_all = self.lda.get_topic_terms(topicid=topic_id, topn=20)
            term_distribute = term_distribute_all[:]
            nums = len(term_distribute)
            # print("topic: " + str(topic_id) + ' has ' + str(nums) + 'words')
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
        text = relevant_tenders['Text']
        token = nltk.word_tokenize(str(text).lower())
        lemmatizer = nltk.stem.WordNetLemmatizer()
        pos_tagged = nltk.pos_tag(token)

        words = filter_words(pos_tagged, lemmatizer)

        # relevant_tenders['ProcessedText'] = " ".join(words)
        self.word_list.append(words)
        return words

    def extract_keyword(self, data):
        doc_word_dict = []  # value: words
        templist2 = []
        token = nltk.word_tokenize(str(data).lower())
        lemmatizer = nltk.stem.WordNetLemmatizer()
        pos_tagged = nltk.pos_tag(token)
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
        token = nltk.word_tokenize(str(data).lower())
        lemmatizer = nltk.stem.WordNetLemmatizer()
        pos_tagged = nltk.pos_tag(token)

        words = filter_words(pos_tagged, lemmatizer)

        doc_bow = self.dictionary.doc2bow(words)
        doc_topics = self.lda.get_document_topics(doc_bow)
        return doc_topics

    def save_lda_model(self):
        # todo: save the result of lda model including the keywords list
        if self.lda is None:
            return False
        self.lda.save(self.model_file)
        return True

    def load_lda_model(self):
        lda_model = gensim.models.ldamodel.LdaModel.load(self.model_file)
        return lda_model

    def add_lda_result_to_data(self):
        self.relevant_tenders['keywords'] = self.relevant_tenders.apply(self.extract_keyword, axis=1)
        self.relevant_tenders['topics'] = self.relevant_tenders.apply(self.get_doc_topic, axis=1)

    def make_result_to_file(self, filepath=None):
        if filepath is None:
            print("Do not find this file!")
            return False
        else:
            self.add_lda_result_to_data()
            self.relevant_tenders.to_csv(filepath, encoding='utf-8_sig')

    def save_topics_to_file(self, num_words, filepath=None):
        if filepath is None:
            print("Do not find this file!")
            return False
        else:
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
            df = pd.DataFrame.from_dict(topic_dic, orient='index',
                                        columns=['keyword' + str(i) for i in range(num_words)])
            df.to_csv(filepath)


if __name__ == '__main__':
    input_df = pd.read_csv(TENDERS_INFO_PATH)
    input_df['Text'] = input_df['Title'] + ' / ' + input_df['Description']
    lda = LDAModel(input_df)
    lda.build_lda_model()

    # just print for demo, will save to file when the model is well enough
    lda.make_result_to_file(filepath='../assets/matching_result_by_lda.csv')

    lda.save_topics_to_file(num_words=20, filepath=TENDERS_TOPIC_PATH)
