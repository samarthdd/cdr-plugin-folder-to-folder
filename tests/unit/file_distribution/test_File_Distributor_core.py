import os
import sys
from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, folder_create, file_copy,folder_delete_all

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.file_distribution.File_Distributor import File_Distributor
from cdr_plugin_folder_to_folder.utils.testing.Temp_Config import Temp_Config
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from cdr_plugin_folder_to_folder.processing.File_Processing import File_Processing
from cdr_plugin_folder_to_folder.processing.Loops import Loops
from cdr_plugin_folder_to_folder.utils.testing.Direct_API_Server import Direct_API_Server
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data
from cdr_plugin_folder_to_folder.pre_processing.Hash_Json import Hash_Json

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

class test_File_Distributor(Temp_Config):

    def setUp(self) -> None:
        self.file_distributor = File_Distributor()

    pre_processor = None
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Direct_API_Server().setup()

        cls.hash_json      = Hash_Json()
        cls.test_data      = Test_Data()
        cls.test_file      = cls.test_data.image()
        cls.pre_processor = Pre_Processor()
        #cls.pre_processor.clear_data_and_status_folders()
        cls.stage_1       = cls.pre_processor.process(cls.test_file)
        cls.hash_json.save()
        cls.stage_2       = Loops().LoopHashDirectories()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.pre_processor.clear_data_and_status_folders()
        folder_delete_all(os.path.join(os.getcwd(), "zip_folder"))

    def test__init__(self):
        assert self.file_distributor.config             is   not None
        assert self.file_distributor.hd1_base_location  is   not None
        assert self.file_distributor.hd2_base_location  is   not None
        assert self.file_distributor.hd3_base_location  is   not None

    # def test_get_hd1_files(self):
    #     response=self.file_distributor.get_hd1_files(1)
    #     assert response  is not None
    #     assert os.path.exists(response)
    #
    # def test_get_hd3_files(self):
    #     response = self.file_distributor.get_hd3_files(1)
    #     assert response is not None
    #     assert os.path.exists(response)
    #
    # def test_get_hd2_metadata_files(self):
    #     response = self.file_distributor.get_hd2_metadata_files(1)
    #     assert response is not None
    #     assert os.path.exists(response)
    #
    # def test_get_hd2_source_files(self):
    #     response = self.file_distributor.get_hd2_source_files(1)
    #     assert response is not None
    #     assert os.path.exists(response)
    #
    # def test_get_hd2_hash_folder_list(self):
    #     response = self.file_distributor.get_hd2_hash_folder_list(1)
    #     assert response is not None
    #     assert os.path.exists(response)
    #
    # def test_get_hd2_report_file(self):
    #     response = self.file_distributor.get_hd2_report_files(1)
    #     assert response is not None
    #     assert os.path.exists(response)

    def test_get_hd2_status_hash_file(self):
        response = self.file_distributor.get_hd2_status_hash_file()
        assert response is not None
        assert os.path.exists(response)

