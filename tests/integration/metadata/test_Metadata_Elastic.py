from unittest import TestCase
from unittest.mock import patch, call

import pytest
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import temp_file, file_delete, temp_folder, folder_delete_all, file_name
from osbot_utils.utils.Json import json_load_file

from cdr_plugin_folder_to_folder.metadata.Metadata import Metadata
from cdr_plugin_folder_to_folder.metadata.Metadata_Elastic import Metadata_Elastic
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing


class test_Metadata_Elastic(TestCase):
    test_file = None
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_file            = temp_file(contents='Static text so that we have a static hash')
        cls.file_hash            = '500286533bf75d769e9180a19414d1c3502dd52093e7351a0a9b1385d8f8961c'
        cls.test_metadata        = Metadata()
        cls.test_metadata.add_file(cls.test_file)
        assert cls.test_metadata.exists()

    @classmethod
    def tearDownClass(cls) -> None:
        file_delete(cls.test_file)

    def setUp(self) -> None:
        self.metadata_elastic = Metadata_Elastic()
        self.metadata_service = Metadata_Service()
        self.metadata_service.metadata_elastic = self.metadata_elastic
        Setup_Testing().configure_metadata_elastic(self.metadata_elastic)

        if self.metadata_elastic.enabled is False:
            pytest.skip('Elastic server not available')

        self.test_metadata_folder = self.test_metadata.metadata_folder_path()

        Pre_Processor().clear_data_and_status_folders()

    def test_add_metadata(self):
        metadata            = self.metadata_service.create_metadata(file_path=self.test_file)
        metadata_data       = metadata.data
        original_hash       = metadata.original_hash()
        result_add_metadata = self.metadata_elastic.add_metadata(metadata_data)

        assert original_hash == self.file_hash
        assert result_add_metadata.get('_shards').get('successful') == 1

        assert self.metadata_elastic.get_metadata   (original_hash=original_hash)               == metadata_data
        assert self.metadata_elastic.delete_metadata(original_hash=original_hash).get('result') == 'deleted'
        assert self.metadata_elastic.get_metadata   (original_hash=original_hash)               == {}

    def test_clear_all_metadata(self):
        self.metadata_elastic.delete_all_metadata()
        assert len(self.metadata_elastic.get_all_metadata()) == 0

    def test_get_from_file(self):
        metadata = self.metadata_service.create_metadata(file_path=self.test_file)
        metadata_data = self.metadata_service.get_from_file(metadata.metadata_folder_path())

        assert self.metadata_service.metadata_folder == self.test_metadata_folder
        assert metadata_data == {   'file_name'              : file_name(self.test_file) ,
                                    'xml_report_status'      : None                      ,
                                    'last_update_time'       : None                      ,
                                    'rebuild_server'         : None                      ,
                                    'server_version'         : None                      ,
                                    'error'                  : None                      ,
                                    'original_file_paths'    : [ self.test_file]         ,
                                    'original_hash'          : self.file_hash            ,
                                    'original_file_extension': None                      ,
                                    'original_file_size'     : None                      ,
                                    'rebuild_file_path'      : None                      ,
                                    'rebuild_hash'           : None                      ,
                                    'rebuild_status'         : FileStatus.INITIAL.value  ,
                                    'rebuild_file_extension' : None                      ,
                                    'rebuild_file_size'      : None                      ,
                                    'rebuild_file_duration'  : None
                                    }

        metadata.delete()

    def test_get_metadata_file_path(self):
        self.metadata_service.metadata_folder = self.test_metadata.metadata_folder_path()
        assert self.metadata_service.get_metadata_file_path() == self.test_metadata.metadata_file_path()

    def test_setup(self):
        self.metadata_elastic.setup()
        assert self.metadata_elastic.index_name in self.metadata_elastic.elastic().elastic().index_list()

    @patch('cdr_plugin_folder_to_folder.metadata.Metadata_Elastic.Metadata_Elastic.add_metadata')
    def test_write_metadata_to_file(self, mock_add_metadata):
        expected_metadata = { 'file_name'           : file_name(self.test_file) ,
                              'original_file_paths' : [self.test_file]          ,
                              'original_hash'       : self.file_hash            ,
                              'rebuild_hash'        : None                      ,
                              'rebuild_status'      : 'Initial'                 ,
                              'xml_report_status'   : None                      ,
                              'target_path'         : None                      ,
                              'error'               : None                      }
        metadata_folder = temp_folder()
        metadata        = self.test_metadata.data
        self.metadata_service.write_metadata_to_file(metadata, metadata_folder)
        assert json_load_file(self.metadata_service.get_metadata_file_path()) == expected_metadata
        assert mock_add_metadata.mock_calls == [call(expected_metadata)]
        folder_delete_all(metadata_folder)










