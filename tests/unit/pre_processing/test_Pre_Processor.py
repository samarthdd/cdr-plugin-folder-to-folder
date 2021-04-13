import os
import sys
from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, folder_create, file_copy, files_list

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from cdr_plugin_folder_to_folder.utils.Log_Duration import log_duration
from cdr_plugin_folder_to_folder.utils.Logging import log_debug
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing
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

        metadata_elastic = self.pre_processor.meta_service.metadata_elastic
        Setup_Testing().set_config_for_local_testing(config=metadata_elastic.elastic().config)
        metadata_elastic.setup()
        assert metadata_elastic.elastic().enabled

        

    def tearDown(self) -> None:
        pass


    def test__init__(self):
        assert folder_exists(self.pre_processor.data_target  )
        assert folder_exists(self.pre_processor.status_target)
        assert folder_exists(self.path_h1)

    @log_duration
    def test_process_files(self):
        path_data   = self.pre_processor.data_target
        path_status = self.pre_processor.status_target
        self.pre_processor.clear_data_and_status_folders()

        assert len(files_list(path_data   )) == 0
        assert len(files_list(path_status )) == 0
        assert len(files_list(self.path_h1)) > 0


        self.pre_processor.process_files()

        assert len(files_list(path_data  )) > 0
        assert len(files_list(path_status)) == 1



    def test_process_file(self):
        source_file = self.test_data.images().pop()
        self.pre_processor.process(source_file)
        assert folder_exists(self.pre_processor.dst_folder)

