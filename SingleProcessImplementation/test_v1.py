import os

from datetime import datetime

from data_clean import PreProcess
from build_lda_mallet import BuildLDAModel

path_in = os.getcwd() + '/extracted_risk_factors'
path_out = os.getcwd() + '/topic_modelling_risk_outputs'


class topic_modelling(object):
    def __init__(self):
        self.preprocess = PreProcess()
        self.open_and_process()

    def open_and_process(self):
        print('Initiating data pre-processing...')
        for filename in os.listdir(path_in):
            word_bag = []
            print('Current file: ', filename)
            self.filename = filename
            with open(path_in + '/' + filename, 'r', encoding='utf-8') as f:
                file_contents = f.read().strip()
                file_contents = self.preprocess.multi_word_exp(file_contents)
                file_contents = self.preprocess.replace_unicode(file_contents)
                for para in file_contents:
                    para = para.lower()
                    temp_word_bag = self.preprocess.process_para(para)
                    if temp_word_bag:
                        word_bag.append(temp_word_bag)
                        # if 'item 1a' not in para and 'item 1b' not in para and 'tableofcontents' not in para:
                        #     print(para)
                        #     temp_word_bag = self.preprocess.process_para(para)
                        #     if temp_word_bag:
                        #         word_bag.append(temp_word_bag)
                        # else:
                        #     print(para)
                        #     if 'item 1a' in para:
                        #         if len(para) > 300:
                        #             para = para.replace('item 1a', '')
                        #         else:
                        #             para = None
                        #     if 'item 1b' in para:
                        #         if len(para) > 300:
                        #             para = para.replace('item 1b', '')
                        #         else:
                        #             para = None
                        #     if 'tableofcontents' in para:
                        #         para.replace('tableofcontents','')
                        #     if para:
                        #         temp_word_bag = self.preprocess.process_para(para)
                        #         if temp_word_bag:
                        #             word_bag.append(temp_word_bag)
                # no_of_topics = len(word_bag)
                no_of_topics = len(self.preprocess.remove_duplicates(word_bag))
                if no_of_topics < 3:
                    no_of_topics = 3
                elif no_of_topics > 30:
                    no_of_topics = 30
                print('Done pre-processing!')
                self.build_mallet = BuildLDAModel(word_bag, no_of_topics)
                self.write_file()
        print('Done!')

    def write_file(self):
        print('Initiating file write...')
        # filename_list = filename.split('_')
        # NameCompanyTicker = filename_list[0]
        # FilingType = filename_list[2]
        # FilingDate = filename_list[5]
        lda_topics = self.build_mallet.topics
        doc_topics = self.build_mallet.doc_topics
        topic_keys = self.build_mallet.topic_keys
        if lda_topics and doc_topics and topic_keys:
            doc_topic_content = open(doc_topics, 'r').read()
            topic_keys_content = open(topic_keys, 'r').read()
        else:
            doc_topic_content = ''
            topic_keys_content = ''
        with open(path_out + '/' + self.filename[0:-4] + '_doc_topics.txt', 'w') as f:
            f.write(doc_topic_content)
        with open(path_out + '/' + self.filename[0:-4] + '_topic_keys.txt', 'w') as f:
            f.write(topic_keys_content)
        with open(path_out + '/' + self.filename[0:-4] + '_lda_topics.txt', 'w') as f:
            f.write(str(lda_topics))
        print('File write successful')


if __name__ == '__main__':
    dt = datetime.now()
    topic_modelling()
    dt1 = datetime.now()
    if (dt1 - dt).seconds <= 120:
        print('Total time taken :- ', (dt1 - dt).seconds, 'seconds')
    else:
        minutes = (dt1 - dt).seconds / 60
        print('Total time taken :- ', minutes)
