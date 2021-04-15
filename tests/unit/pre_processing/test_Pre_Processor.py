import os
import sys
from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, folder_create, file_copy, files_list, temp_file, file_delete, \
    temp_folder, folder_delete_all

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.metadata.Metadata import Metadata
from cdr_plugin_folder_to_folder.metadata.Metadata_Utils import Metadata_Utils
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from cdr_plugin_folder_to_folder.utils.Log_Duration import log_duration
from cdr_plugin_folder_to_folder.utils.Logging import log_debug
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

class test_Pre_Processor(TestCase):
    test_file = None
    temp_hd1  = None
    file_hash = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_file     = temp_file(contents='Static text so that we have a static hash')
        cls.file_hash     = '500286533bf75d769e9180a19414d1c3502dd52093e7351a0a9b1385d8f8961c'
        cls.temp_hd1      = temp_folder()
        cls.pre_processor = Pre_Processor()
        Setup_Testing().configure_pre_processor(cls.pre_processor)

    @classmethod
    def tearDownClass(cls) -> None:
        file_delete      (cls.test_file)
        folder_delete_all(cls.temp_hd1 )
        Metadata(file_hash=cls.file_hash).delete()

    def setUp(self) -> None:

        #self.test_data     = Test_Data()
        #self.test_file     = self.test_data.image()
            self.pre_processor.clear_data_and_status_folders()

        #self.path_h1       = self.pre_processor.config.hd1_location
        #self.path_h2       = self.config.hd2_location
        #self.path_h3       = self.config.hd3_location
        #folder_create(self.path_h1)




    def tearDown(self) -> None:
        pass


    def test__init__(self):
        assert folder_exists(self.pre_processor.storage.hd2_data()  )
        assert folder_exists(self.pre_processor.storage.hd2_status())
        #assert folder_exists(self.path_h1)

    def test_file_hash(self):
        assert self.pre_processor.file_hash(self.test_file) == self.file_hash

    #def test_file_metadata(self):

    def test_process_files(self):
        path_data   = self.pre_processor.storage.hd2_data()
        path_status = self.pre_processor.storage.hd2_status()

        assert len(files_list(path_data   )) == 0
        assert len(files_list(path_status )) == 0
        #assert len(files_list(self.path_h1)) > 0


        self.pre_processor.process_files()

        assert len(files_list(path_data  )) > 0
        assert len(files_list(path_status)) == 1



    def test_process_file(self):
        metadata = Metadata(file_hash=self.file_hash)
        assert metadata.exists() is False
        #source_file = self.test_data.images().pop()
        self.pre_processor.process(self.test_file)
        assert metadata.exists() is True


