from gensim import corpora, models
from data_clean import execute


def ldaModel(word_bag):
    dictionary = corpora.Dictionary(word_bag)
    # print(dictionary)
    corpus = [dictionary.doc2bow(word) for word in word_bag]
    # print(corpus)
    lda_model = models.ldamodel.LdaModel(corpus, num_topics=100, id2word=dictionary, passes=20)
    print(lda_model)


if __name__ == "__main__":
    word_bag = execute()
    ldaModel(word_bag)
