import os
import sys
from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, folder_create, file_copy

from cdr_plugin_folder_to_folder.common_settings.config_params import Config
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

class test_Pre_Processor(TestCase):

    def setUp(self) -> None:
        self.pre_processor = Pre_Processor()
        self.test_data     = Test_Data()
        self.test_file     = self.test_data.image()
        self.config        = Config().load_values()
        self.path_h1       = self.config.hd1_location
        self.path_h2       = self.config.hd2_location
        self.path_h3       = self.config.hd3_location
        folder_create(self.path_h1)
        

    def tearDown(self) -> None:
        pass


    def test__init__(self):
        assert folder_exists(self.pre_processor.data_target  )
        assert folder_exists(self.pre_processor.status_target)
        assert folder_exists(self.path_h1)

    def test_process_files(self):
        self.pre_processor.process_files()

        data_path        = self.pre_processor.data_target
        status_path      = self.pre_processor.status_target

        data_directory   = os.listdir(data_path)
        status_directory = os.listdir(status_path)

        assert len(data_directory) is not 0
        assert len(status_directory) is not 0

    def test_process_file(self):
        source_file = self.test_data.images().pop()
        self.pre_processor.process(source_file)
        assert folder_exists(self.pre_processor.dst_folder)

