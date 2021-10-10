"""
this is only used for test
"""

from Matcher.get_doc_vectors import get_d2v

d2v = get_d2v('../Out/doc2vec-300.model')
print(d2v.wv.most_similar('health'))