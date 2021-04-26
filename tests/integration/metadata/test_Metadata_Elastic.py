from unittest import TestCase
from unittest.mock import patch, call

import pytest
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import temp_file, file_delete, temp_folder, folder_delete_all, file_name
from osbot_utils.utils.Json import json_load_file

from cdr_plugin_folder_to_folder.metadata.Metadata import Metadata
from cdr_plugin_folder_to_folder.metadata.Metadata_Elastic import Metadata_Elastic
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.pre_processing.Hash_Json import Hash_Json
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from cdr_plugin_folder_to_folder.pre_processing.Status import FileStatus
from cdr_plugin_folder_to_folder.utils.Logging_Process import process_all_log_entries_and_end_logging_process
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing
from cdr_plugin_folder_to_folder.utils.testing.Temp_Config import Temp_Config


class test_Metadata_Elastic(Temp_Config):
    test_file = None
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.test_file            = temp_file(contents='Static text so that we have a static hash')
        cls.file_hash            = '500286533bf75d769e9180a19414d1c3502dd52093e7351a0a9b1385d8f8961c'
        cls.metadata_elastic     = Metadata_Elastic()
        Setup_Testing().configure_metadata_elastic(cls.metadata_elastic)
        cls.metadata_service = Metadata_Service()
        cls.metadata_service.metadata_elastic = cls.metadata_elastic

        if cls.metadata_elastic.enabled is False:
            pytest.skip('Elastic server not available')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        file_delete(cls.test_file)

    def setUp(self) -> None:
        self.storage.hd1_delete_all_files()
        self.storage.hd2_delete_all_files()
        # assert cls.test_metadata.exists()

        #self.test_metadata_folder = self.test_metadata.metadata_folder_path()

        #Pre_Processor().clear_data_and_status_folders()
        pass

    def test_add_metadata(self):
        metadata            = self.metadata_service.create_metadata(file_path=self.test_file)
        metadata_data       = metadata.data
        original_hash       = metadata.get_original_hash()
        result_add_metadata = self.metadata_elastic.add_metadata(metadata_data)

        assert original_hash == self.file_hash
        assert result_add_metadata.get('_shards').get('successful') == 1

        elastic_metadata = self.metadata_elastic.get_metadata(original_hash=original_hash)
        local_metadata   = metadata_data

        del elastic_metadata[self.metadata_elastic.time_field]

        assert elastic_metadata == metadata_data
        assert self.metadata_elastic.delete_metadata(original_hash=original_hash).get('result') == 'deleted'
        assert self.metadata_elastic.get_metadata   (original_hash=original_hash)               == {}

    def test_delete_all_metadata(self):
        self.metadata_elastic.delete_all_metadata()
        assert len(self.metadata_elastic.get_all_metadata()) == 0

    def test_reload_metadatas(self):
        count = 2
        self.add_test_files(count=count,execute_stage_1=True)
        assert self.metadata_elastic.reload_metadatas() == count

    def test_reset_elastic_data(self):
        hash_json = Hash_Json()
        count     = 10              # use 1000
        text_size = 500             # use 50000
        self.add_test_files(count=count, text_size=text_size, execute_stage_1=True)
        message = self.metadata_elastic.reload_elastic_data()
        assert message == f'Elastic files_metadata has been reset and {count} metadata items reloaded'
        assert len(hash_json.get_from_file()) == count






    # @log_duration
    # def reload_data_from_hd2(self):
    #     return self.storage.hd2_metadatas()
    #
    # def test_reload_data_from_hd2(self):
    #     self.add_test_files(count=1, execute_stage_1=True)
    #     result = self.status.reload_data_from_hd2()
    #     pprint(result)
    #
    #     process_all_log_entries_and_end_logging_process()


    def test_get_from_file(self):
        metadata = self.metadata_service.create_metadata(file_path=self.test_file)
        metadata_data = self.metadata_service.get_from_file(metadata.metadata_folder_path()).data

        #assert self.metadata_service.metadata_folder == self.test_metadata_folder
        metadata_data['last_update_time'] = None
        assert metadata_data == {   'file_name'              : file_name(self.test_file) ,
                                    'xml_report_status'      : None                      ,
                                    'last_update_time'       : None                      ,
                                    'rebuild_server'         : None                      ,
                                    'server_version'         : None                      ,
                                    'error'                  : None                      ,
                                    'original_file_paths'    : [ self.test_file]         ,
                                    'original_hash'          : self.file_hash            ,
                                    'original_file_extension': '.tmp'                     ,
                                    'original_file_size'     : 41                        ,
                                    'rebuild_file_path'      : None                      ,
                                    'rebuild_hash'           : None                      ,
                                    'rebuild_status'         : FileStatus.INITIAL        ,
                                    'rebuild_file_extension' : None                      ,
                                    'rebuild_file_size'      : None                      ,
                                    'rebuild_file_duration'  : None                      ,
                                    'f2f_plugin_version'     : None                      ,
                                    'f2f_plugin_git_commit'  : None
                                }

        metadata.delete()

    def test_get_metadata_file_path(self):
        self.test_metadata = Metadata()
        self.test_metadata.add_file(self.test_file)
        self.metadata_service.metadata_folder = self.test_metadata.metadata_folder_path()
        assert self.metadata_service.get_metadata_file_path() == self.test_metadata.metadata_file_path()
        self.test_metadata.delete()

    def test_setup(self):
        self.metadata_elastic.setup()
        assert self.metadata_elastic.index_name in self.metadata_elastic.elastic().elastic().index_list()









