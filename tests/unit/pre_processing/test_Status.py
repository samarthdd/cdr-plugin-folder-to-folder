import inspect

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import path_combine, temp_file
from osbot_utils.utils.Json  import json_load_file
from osbot_utils.utils.Misc import random_text

from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from cdr_plugin_folder_to_folder.pre_processing.Status import FileStatus, Status
from cdr_plugin_folder_to_folder.utils.testing.Temp_Config import Temp_Config


class test_Status(Temp_Config):

    def setUp(self) -> None:
        self.status  = Status()
        self.storage = self.status.storage

    def test__FileStatus(self):
        assert inspect.getmembers(FileStatus, lambda a: type(a) is str) == [  ('COMPLETED'   , 'Completed Successfully'                           ),
                                                                              ('FAILED'      , 'Completed with errors'                            ),
                                                                              ('INITIAL'     , 'Initial'                                          ),
                                                                              ('IN_PROGRESS' , 'In Progress'                                      ),
                                                                              ('NONE'        , 'None'                                             ),
                                                                              ('TO_PROCESS'  , 'To Process'                                       ),
                                                                              ('__module__'  , 'cdr_plugin_folder_to_folder.pre_processing.Status')]

    def test_load_data(self):
        status = self.status
        assert status.data()             == status.default_data()
        assert status.load_data().data() == status.default_data()
        assert status.get_files_count()  == 0
        for i in range(1,100):
            assert status.add_completed()
            assert status.get_current_status() == FileStatus.COMPLETED
            assert status.get_completed() == i

            assert status.add_failed()
            assert status.get_current_status() == FileStatus.FAILED
            assert status.get_failed() == i

            assert status.add_file()
            assert status.get_current_status() == FileStatus.INITIAL
            assert status.get_files_count() == i

            assert status.add_in_progress()
            assert status.get_current_status() == FileStatus.IN_PROGRESS
            assert status.get_in_progress() == 1

            assert status.add_to_be_processed()
            assert status.get_current_status() == FileStatus.TO_PROCESS
            assert status.get_files_to_process() == i


        assert json_load_file(status.status_file_path()) == status.data()

    def test_reload_data_from_hd2(self):
        temp_file_1 = temp_file(contents=random_text())
        temp_file_2 = temp_file(contents=random_text())
        Pre_Processor().process_files()
        result = self.status.reload_data_from_hd2()
        pprint(result)


    def test_status_file_path(self):
        assert self.status.status_file_path() == path_combine(self.storage.hd2_status(), Status.STATUS_FILE_NAME)



    # todo: add multi-threading test
    # def worker(c):
    #     for i in range(2):
    #         r = random.random()
    #         logging.debug('Sleeping %0.02f', r)
    #         time.sleep(r)
    #         c.increment()
    #     logging.debug('Done')
    #
    # if __name__ == '__main__':
    #     counter = Counter()
    #     for i in range(2):
    #         t = threading.Thread(target=worker, args=(counter,))
    #         t.start()
    #
    #     logging.debug('Waiting for worker threads')
    #     main_thread = threading.currentThread()
    #     for t in threading.enumerate():
    #         if t is not main_thread:
    #             t.join()
    #     logging.debug('Counter: %d', counter.value)