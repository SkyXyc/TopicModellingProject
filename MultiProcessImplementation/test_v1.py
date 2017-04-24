import os

from datetime import datetime
from process_init import MyProcess

path_in = os.getcwd() + '/extracted_risk_factors'
path_out = os.getcwd() + '/topic_modelling_risk_outputs'


class TopicModelling(object):
    def __init__(self):
        self._process_count = 0
        self._process_list = []
        self.open_and_process()

    def open_and_process(self):
        print('Initiating ...')
        for filename in os.listdir(path_in):
            if self._process_count >= 64:
                self.processes_check()
            process_id = MyProcess(filename, path_in, path_out)
            process_id.start()
            self._process_count += 1
            self._process_list.append(process_id)

        self.processes_check()

    def processes_check(self):
        # for p_id in self._process_list:
        #     p_id.join()
        for p_id in range(len(self._process_list)):
            if not self._process_list[p_id].is_alive():
                self._process_list.pop(p_id)
                self._process_count -= 1
            if self._process_count < 64:
                return True


if __name__ == '__main__':
    dt = datetime.now()
    try:
        main_thread_object = TopicModelling()
    except Exception as e:
        with open('errors.txt') as f:
            f.write(str(e))
    process_list = main_thread_object._process_list
    for pid in range(len(process_list)):
        process_list[pid].join()
    dt1 = datetime.now()
    if (dt1 - dt).seconds <= 120:
        print('Total time taken :- ', (dt1 - dt).seconds, 'seconds')
    else:
        minutes = (dt1 - dt).seconds / 60
        print('Total time taken :- ', minutes)
