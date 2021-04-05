import os
import sys
from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, folder_create, file_copy

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.processing.Loops import Loops
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

class test_Processor(TestCase):

    def setUp(self) -> None:
        self.config         = Config().load_values()
        self.repotrs_path   = os.path.join(self.config.hd2_location,"reports")
        self.processed_path = os.path.join(self.config.hd2_location,"processed")


    def tearDown(self) -> None:
        pass

    def test__init__(self):
        assert folder_exists(self.config.hd1_location)

    def test_process_files(self):
        Loops.LoopHashDirectories()

        assert folder_exists(self.repotrs_path)
        assert folder_exists(self.processed_path)

    def test_process_file(self):
        pass

