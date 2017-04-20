import os
import spacy
import nltk

from nltk import word_tokenize
from nltk.corpus import stopwords, wordnet as wn
from nltk.stem import WordNetLemmatizer

path = os.getcwd() + '/Risk/correct/training'


# stop_words = stopwords.words('english')
# nlp = spacy.load('en')

class PreProcess(object):
    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.nlp = spacy.load('en')

    def hypernym(self, _word):
        sets = wn.synsets(_word)
        # print(word , "***", sets)
        # for set in sets:
        #     for hyper in set.hypernyms():
        # print(word, set, hyper)
        # print("________________")
        pass

    def pos_tag(self):
        return nltk.pos_tag(self._tokens, tagset='universal')

    def multi_word_exp(self, _file_contents):
        doc = self.nlp(_file_contents)
        # print(doc)
        if doc.ents:
            for entity in doc.ents:
                # print(entity.label_, entity.text)
                if ' ' in entity.text:
                    _file_contents = _file_contents.replace(entity.text, entity.text.replace(" ", ''))
        # for ent in doc.ents:
        #                 entities.append(ent.text)
        #                 print(entities)
        #             for item in doc:
        #                 # print(item.text)
        #                 for entity in doc.ents:
        #                     if item.text in entity.text:
        #                         print(item.text, item.ent_iob, item.ent_type_)
        #
        #             for item in doc.ents:
        #                 print(item.merge('_'))
        # for item in doc.ents:
        #     print(item.text, item.label_)
        return _file_contents

    def lemmatize(self, _word, _tag):
        wordnet_lemmatizer = WordNetLemmatizer()
        # default pos tag is 'n'. If anything else see below eg
        # eg: wordnet_lemmatizer.lemmatize(_word, pos=’v’)
        # ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
        _tag_map = {'ADJ': 'a', 'ADV': 'r', 'NOUN': 'n', 'VERB': 'v'}
        if _tag in _tag_map.keys():
            _tag = _tag_map[_tag]
        else:
            _tag = 'n'
        return wordnet_lemmatizer.lemmatize(_word, pos=_tag)

    def process(self, _word, _tag):
        _word = _word.lower()
        _word = ''.join(char for char in _word if char.isalpha())
        # print(_word)
        #     print(_word)
        if _word not in self.stop_words:
            if not _word.isnumeric() and _word:
                _word = self.lemmatize(_word, _tag)
                self.hypernym(_word)
                if len(_word) > 1:
                    return _word
        return None
        # temp_word_bag.append(_word)
        # print(_word, nltk.pos_tag([_word]))
        # print()
        # return _word
        # word_bag.append(temp_word_bag)

    def remove_duplicates(self, _word_bag):
        _new_word_bag = []
        for item in _word_bag:
            if item not in _new_word_bag:
                _new_word_bag.append(item)
        return _new_word_bag

    def replace_unicode(self, _file_contents):
        if '\xa0' in _file_contents:
            _file_contents = _file_contents.replace('\xa0', '\n')
        _file_contents = _file_contents.split('\n\n\n\n\n\n\n\n\n\n')
        return _file_contents

    def process_para(self, _para):
        _temp_word_bag = []
        self._tokens = word_tokenize(_para)
        _tags = self.pos_tag()
        for item in _tags:
            _word = item[0]
            _tag = item[1]
            _word = self.process(_word, _tag)
            if _word and _word not in ('item', 'tableofcontents'):
                _temp_word_bag.append(_word)
        return _temp_word_bag


        # def execute(self):
        #     print('Initiating data pre-processing...')
        #     word_bag = []
        #     for filename in os.listdir(path_in):
        #         print('Current file: ', filename)
        #         with open(path_in + '/' + filename, 'r', encoding='utf-8') as f:
        #             temp_word_bag = []
        #             file_contents = f.read().strip()
        #             file_contents = self.multi_word_exp(file_contents)
        #             tokens = word_tokenize(file_contents)
        #             tags = self.pos_tag(tokens)
        #             # print(tags)
        #             for item in tags:
        #                 word = item[0]
        #                 tag = item[1]
        #                 word = self.process(word, tag)
        #                 if word:
        #                     temp_word_bag.append(word)
        #         word_bag.append(temp_word_bag)
        #         print('Done!')
        #     # print(len(word_bag_1))
        #     # print(word_bag, len(word_bag))
        #     #
        #     # with open('word_bag.txt', 'w') as f:
        #     #     line = ''
        #     #     for word in word_bag:
        #     #         line += word + ','
        #     #     f.write(line[0:-1])
        #     print('Done pre-processing!')
        #     return word_bag


if __name__ == '__main__':
    pass
    # p1 = PreProcess()
    # p1.execute()
