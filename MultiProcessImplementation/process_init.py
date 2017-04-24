import multiprocessing
from build_lda_mallet import BuildLDAModel
from data_clean import PreProcess


class MyProcess(multiprocessing.Process):
    def __init__(self, _filename, _path_in, _path_out):
        print('Creating process: ', _filename)
        multiprocessing.Process.__init__(self)
        self._filename = _filename
        self._no_of_topics = 0
        self._path_in = _path_in
        self._path_out = _path_out
        self._word_bag = []
        self._pre_process = PreProcess()

    def execute(self):
        with open(self._path_in + '/' + self._filename, 'r', encoding='utf-8') as f:
            file_contents = f.read().strip()
            file_contents = self._pre_process.multi_word_exp(file_contents)
            file_contents = self._pre_process.replace_unicode(file_contents)
            for para in file_contents:
                para = para.lower()
                temp_word_bag = self._pre_process.process_para(para)
                if temp_word_bag:
                    self._word_bag.append(temp_word_bag)
            self._no_of_topics = len(self._pre_process.remove_duplicates(self._word_bag))
            if self._no_of_topics < 3:
                self._no_of_topics = 3
            elif self._no_of_topics > 30:
                self._no_of_topics = 30
            print('Done!')

    def run(self):
        print('Starting pre-processing step for file: ', self._filename)
        self.execute()
        print('Starting process for file :-', self._filename)
        self.build_mallet = BuildLDAModel(self._filename, self._word_bag, self._no_of_topics)
        self.write_file()

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
        with open(self._path_out + '/' + self._filename[0:-4] + '_doc_topics.txt', 'w') as f:
            f.write(doc_topic_content)
        with open(self._path_out + '/' + self._filename[0:-4] + '_topic_keys.txt', 'w') as f:
            f.write(topic_keys_content)
        with open(self._path_out + '/' + self._filename[0:-4] + '_lda_topics.txt', 'w') as f:
            f.write(str(lda_topics))
        print('File write successful')
