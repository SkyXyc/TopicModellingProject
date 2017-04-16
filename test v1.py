import os

from datetime import datetime
from gensim import corpora, models

from data_clean import execute


def build_corpus(_word_bag):
    print('Building dictionary...')
    _dictionary = corpora.Dictionary(_word_bag)
    print('Done building dictionary!')
    # print(dictionary)
    print('Building corpus...')
    _corpus = [_dictionary.doc2bow(word) for word in _word_bag]
    print('Done building corpus!')
    # print(corpus)
    return _corpus, _dictionary


def ldaModel(_corpus, _dictionary):
    print('--------------------Training LDA Model--------------------')
    lda_model = models.ldamodel.LdaModel(corpus=_corpus, num_topics=100, id2word=_dictionary, passes=20)
    print(lda_model, '\n')
    print('--------------------------Done!--------------------------')
    _topics = lda_model.show_topics(num_topics=100, num_words=5, formatted=False)
    return _topics


def ldaMallet(_corpus, _dictionary):
    """class gensim.models.wrappers.ldamallet.LdaMallet(mallet_path, _corpus=None, num_topics=100, alpha=50,
    id2word=None, workers=4, prefix=None, optimize_interval=0, iterations=1000, topic_threshold=0.0) """
    print('--------------------Training LDA Mallet Model--------------------')
    model = models.wrappers.LdaMallet(os.getcwd() + '/mallet-2.0.8/bin/mallet', corpus=_corpus, id2word=_dictionary)
    model.convert_input(corpus=_corpus)
    print('----------------------------Done!----------------------------')
    # print(model.corpus2mallet(_corpus,'data.mallet'))
    print('document topics @', model.fdoctopics())
    print('topic keys @', model.ftopickeys())
    print('word weights @', model.fwordweights())
    _topics = model.show_topics(num_topics=100, num_words=5, formatted=False)
    return _topics


if __name__ == "__main__":
    dt = datetime.now()
    word_bag = execute()
    corpus, dictionary = build_corpus(_word_bag=word_bag)
    ldaModel(_corpus=corpus, _dictionary=dictionary)
    ldaMallet(_corpus=corpus, _dictionary=dictionary)
    dt1 = datetime.now()
    print('Time taken :- ', (dt1 - dt).seconds, 'seconds')
