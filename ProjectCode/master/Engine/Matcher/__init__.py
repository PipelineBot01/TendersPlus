"""
Matcher is used to match tenders and researchers via their labels, category, descriptions or interest

Authors:
- Yuxuan Yang u7078049
- name uid
- name uid
"""

from gensim.models.doc2vec import Doc2Vec
# if you want to switch model,use look up config.py
import Matcher.config


class Doc2vecMatcher:
    def __init__(self, model, type):
        """
        :params model: word embedding model
        :params type: doc2vec/ word2vec
        """
        self.model = model
        self.type = type

    def match(self, inputs, topn=10):
        """
        :params inputs: the inputs are the tags or description of researchers, inputs: list of words
        :params tonp: the top n similar tenders

        return: a list of  (ATM ID, similarity)
        """
        # TODO: currently use doc2vec as the default model
        input_vec = self.model.infer_vector(inputs,alpha=0.001,epochs=5000)
        match_result = self.model.dv.most_similar(input_vec, topn=topn)
        return match_result



class KeyBertMatcher:
    def __init__(self,):
        pass



if __name__ == "__main__":
    # ===== load default d2v model =====
    d2v = Doc2Vec.load(config.d2v_model_300)
