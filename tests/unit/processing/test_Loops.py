import asyncio
from unittest import TestCase

from osbot_utils.utils.Dev import pprint


from cdr_plugin_folder_to_folder.processing.Loops import Loops
from cdr_plugin_folder_to_folder.utils.Logging import log_info, log_debug
from cdr_plugin_folder_to_folder.utils.Logging_Process import start_logging
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing
from cdr_plugin_folder_to_folder.utils.testing.Temp_Config import Temp_Config
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data

class test_Loops(Temp_Config):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.test_data = Test_Data()
        cls.test_file = cls.test_data.image()
        cls.pre_processor = Pre_Processor()
        cls.pre_processor.clear_data_and_status_folders()
        cls.stage_1 = cls.pre_processor.process(cls.test_file)
        pass

    def setUp(self) -> None:
        Setup_Testing()
        self.loops = Loops()

    def test_LoopHashDirectories(self):

        assert self.loops.LoopHashDirectories() is True
        log_debug(message='stop_logging', data={'when': 'now'})
        self.log_worker.join()

    def test_LoopHashDirectoriesAsync(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.loops.LoopHashDirectoriesAsync(thread_count=1))

    def test_LoopHashDirectoriesInternal(self):
        self.loops.LoopHashDirectoriesInternal(thread_count=1, do_single=False)

