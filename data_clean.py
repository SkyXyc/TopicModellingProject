import os
from nltk.corpus import stopwords, wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
import spacy


path = os.getcwd()+'\\Risk\\correct\\training'

# file_contents = ''
stop_words = stopwords.words('english')
nlp = spacy.load('en')


# print(stop_words)

def hypernym(word):
    sets = wn.synsets(word)
    # print(word , "***", sets)
    # for set in sets:
    #     for hyper in set.hypernyms():
    # print(word, set, hyper)
    # print("________________")
    pass


def multi_word_exp(file_contents):
    doc = nlp(file_contents)
    # print(file_contents)
    # print(doc)
    # entities = []
    if doc.ents:
        for entity in doc.ents:
            # print(entity.label_, entity.text)
            if ' ' in entity.text:
                file_contents = file_contents.replace(entity.text, entity.text.replace(" ", ''))
                # for ent in doc.ents:
                #     entities.append(ent.text)
                #     print(entities)
                # for item in doc:
                #     # print(item.text)
                #     for entity in doc.ents:
                #         if item.text in entity.text:
                #             print(item.text, item.ent_iob, item.ent_type_)

                # for item in doc.ents:
                #     print(item.merge('_'))
    # for item in doc.ents:
    #     print(item.text, item.label_)
    return file_contents


def lemmatize(word):
    wordnet_lemmatizer = WordNetLemmatizer()
    # default pos tag is 'n'. If anything else see below eg
    # eg: wordnet_lemmatizer.lemmatize(word, pos=’v’)
    word = wordnet_lemmatizer.lemmatize(word)
    return word


def process(word):
    word = word.lower()
    word = ''.join(char for char in word if char.isalpha())
    # print(word)
    #     print(word)
    if word not in stop_words:
        if not word.isnumeric() and word:
            word = lemmatize(word)
            hypernym(word)
            if len(word) > 1:
                return word
    return None
    # temp_word_bag.append(word)
    # print(word, nltk.pos_tag([word]))
    # print()
    # return word
    # word_bag.append(temp_word_bag)


def execute():
    word_bag = []
    for filename in os.listdir(path):
        with open(path + '\\' + filename, 'r', encoding='utf-8') as f:
            temp_word_bag = []
            file_contents = f.read().strip()
            file_contents = multi_word_exp(file_contents)
            word_bag_1 = word_tokenize(file_contents)
            for word in word_bag_1:
                word = process(word)
                if word:
                    temp_word_bag.append(word)
            word_bag.append(temp_word_bag)
    # print(len(word_bag_1))
    # print(word_bag, len(word_bag))
    #
    # with open('word_bag.txt', 'w') as f:
    #     line = ''
    #     for word in word_bag:
    #         line += word + ','
    #     f.write(line[0:-1])
    return word_bag


if __name__ == '__main__':
    execute()
