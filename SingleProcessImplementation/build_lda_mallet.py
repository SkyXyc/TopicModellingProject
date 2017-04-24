import os

from datetime import datetime
from gensim import corpora, models


class BuildLDAModel(object):
    def __init__(self, _word_bag, _no_of_topics):
        # obj = PreProcess()
        # self._word_bag = obj.execute()
        self._word_bag = _word_bag
        self._no_of_topics = _no_of_topics
        self.build_corpus()
        # ldaModel(_corpus=corpus, _dictionary=dictionary)
        self.topics, self.doc_topics, self.topic_keys = self.ldaMallet()

    def build_corpus(self):
        print('Building dictionary...')
        self._dictionary = corpora.Dictionary(self._word_bag)
        print('Done building dictionary!')
        print('Building corpus...')
        self._corpus = [self._dictionary.doc2bow(word) for word in self._word_bag]
        print('Done building corpus!')

    def ldaModel(self):
        print('--------------------Training LDA Model--------------------')
        lda_model = models.ldamodel.LdaModel(corpus=self._corpus, num_topics=self._no_of_topics,
                                             id2word=self._dictionary, passes=20)
        print(lda_model, '\n')
        print('--------------------------Done!--------------------------')
        ldaModel_topics = lda_model.show_topics(num_topics=self._no_of_topics, num_words=10, formatted=True)
        return ldaModel_topics

    def ldaMallet(self):
        """class gensim.models.wrappers.ldamallet.LdaMallet(mallet_path, _corpus=None, num_topics=100, alpha=50,
        id2word=None, workers=4, prefix=None, optimize_interval=0, iterations=1000, topic_threshold=0.0) """
        print('--------------------Training LDA Mallet Model--------------------')
        if self._corpus:
            model = models.wrappers.LdaMallet(os.getcwd() + '/mallet-2.0.8/bin/mallet', corpus=self._corpus,
                                              num_topics=self._no_of_topics, id2word=self._dictionary)
            print('----------------------------Done!----------------------------')
            # print(model.corpus2mallet(_corpus,'data.mallet'))
            # print(model.show_topics(num_words=100,))
            doc_topics = model.fdoctopics()
            print('document topics @', doc_topics)
            topic_keys = model.ftopickeys()
            print('topic keys @', topic_keys)
            word_weights = model.fwordweights()
            print('word weights @', word_weights)
            mallet_topics = model.show_topics(num_topics=self._no_of_topics, num_words=10, formatted=True)
            print("Topics with top words & thier weights are :")
            print(mallet_topics)
            return mallet_topics, doc_topics, topic_keys
        else:
            print('Picked up empty file...')
            return '', '', ''


if __name__ == "__main__":
    dt = datetime.now()
    model = BuildLDAModel()
    # model.build_corpus()
    # corpus, dictionary = build_corpus(_word_bag=word_bag)
    # # ldaModel(_corpus=corpus, _dictionary=dictionary)
    # topics = ldaMallet(_corpus=corpus, _dictionary=dictionary)
    # print("Topics with top words & thier weights are :")
    # print(model)
    dt1 = datetime.now()
    print('Time taken :- ', (dt1 - dt).seconds, 'seconds')
