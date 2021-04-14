import os
import sys
from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, folder_create, file_copy

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from cdr_plugin_folder_to_folder.processing.Loops import Loops
from cdr_plugin_folder_to_folder.utils.Log_Duration import log_duration
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

class test_Processor(TestCase):

    def setUp(self) -> None:
        self.config         = Config()
        self.repotrs_path   = os.path.join(self.config.hd2_location,"reports")
        self.processed_path = os.path.join(self.config.hd2_location,"processed")
        self.pre_processor = Pre_Processor()
        self.loops         = Loops()

    def tearDown(self) -> None:
        pass

    def test__init__(self):
        self.pre_processor.clear_data_and_status_folders()       # clear output folders
        self.pre_processor.process_files()                       # copy files across

        assert folder_exists(self.config.hd1_location)
        assert folder_exists(self.config.hd2_location)
        assert folder_exists(self.config.hd3_location)

    def test_flags(self):
        assert self.loops.IsProcessing() == False
        self.loops.StopProcessing()
        assert self.loops.HasBeenStopped() == True

    @log_duration
    def test_process_file(self):
        self.loops.ProcessSingleFile()
        assert len(os.listdir(self.config.hd3_location)) != 0

    @log_duration
    def test_process_files(self):
        self.loops.LoopHashDirectories()

        assert len(os.listdir(self.config.hd3_location)) != 0

    @log_duration
    def test_processing_inprogress(self):
        Loops.processing_started = True
        assert (False == self.loops.ProcessSingleFile())
        assert (False == self.loops.LoopHashDirectories())


