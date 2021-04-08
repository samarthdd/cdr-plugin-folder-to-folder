import os
import sys
from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, folder_create, file_copy

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.file_distribution.File_Distributor import File_Distributor
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

class test_File_Distributor(TestCase):

    def setUp(self) -> None:
        self.file_distributor = File_Distributor()

    def tearDown(self) -> None:
        pass


    def test__init__(self):
        assert self.file_distributor.config is not None
        assert self.file_distributor.hd1_base_location  is not None
        assert self.file_distributor.hd2_base_location  is not None
        assert self.file_distributor.hd3_base_location  is not None

    def test_get_hd1_files(self):
        response=self.file_distributor.get_hd1_files(1)
        assert response is not None
        assert len(response) is 1

    def test_get_hd3_files(self):
        response = self.file_distributor.get_hd3_files(1)
        assert response is not None
        assert len(response) is 1

    def test_get_hd2_metadata_files(self):
        response = self.file_distributor.get_hd2_metadata_files(1)
        assert response is not None
        assert len(response) is 1

    def test_get_hd2_source_files(self):
        response = self.file_distributor.get_hd2_source_files(1)
        assert response is not None
        assert len(response) is 1

    def test_get_hd2_hash_folder_list(self):
        response = self.file_distributor.get_hd2_hash_folder_list(1)
        assert response is not None
        assert len(response) is 1

    def test_get_hd2_hash_folder_list(self):
        response = self.file_distributor.get_hd2_report_files(1)
        assert response is not None
        assert len(response) is 1

    def test_get_hd2_status_hash_file(self):
        response = self.file_distributor.get_hd2_status_hash_file()
        assert response is not None
        assert len(response) is 1

    def test_configure_hard_discs(self):
        response = self.file_distributor.configure_hard_discs(hd1_path=os.environ.get('HD1_LOCATION'),hd2_path=os.environ.get('HD2_LOCATION'),hd3_path=os.environ.get('HD3_LOCATION'))
        assert response is not None
        assert os.environ.get("MODE") is "1"
        if os.environ.get('MODE',None):
            del os.environ['MODE']


