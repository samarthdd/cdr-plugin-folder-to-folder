from unittest import TestCase
from osbot_utils.utils.Files import file_exists

from cdr_plugin_folder_to_folder.common_settings.Config import API_VERSION
from cdr_plugin_folder_to_folder.utils.testing.Direct_API_Server import Direct_API_Server

class test_File_Distributor(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Direct_API_Server().setup()
        cls.prefix = 'file-distributor'

    def test_hd1(self):
        num_of_files = 1
        path = f"{self.prefix}/hd1/{num_of_files}"
        files = self.client.GET(path)
        assert len(files) == num_of_files
        for file in files:
            assert file_exists(file)

    def test_hd2_metatada(self):
        num_of_files = 1
        path     = f"{self.prefix}/hd2/metadata/{num_of_files}"
        metadata = self.client.GET(path)
        assert metadata == [ '86df34018436a99e1e98ff51346591e189cd76c8518f7288bb1ea8336396259b/metadata.json']

    def test_hd2_source(self):
        num_of_files = 1
        path = f"{self.prefix}/hd2/source/{num_of_files}"
        source = self.client.GET(path)
        assert source == ['86df34018436a99e1e98ff51346591e189cd76c8518f7288bb1ea8336396259b/source']

    def test_hd2_report(self):
        num_of_files = 1
        path = f"{self.prefix}/hd2/report/{num_of_files}"
        source = self.client.GET(path)
        assert source == ['86df34018436a99e1e98ff51346591e189cd76c8518f7288bb1ea8336396259b/report.json']

    def test_hd2_hash_folder_list(self):
        num_of_files = 1
        path = f"{self.prefix}/hd2/hash_folder_list/{num_of_files}"
        folder_list = self.client.GET(path)
        assert folder_list == ['86df34018436a99e1e98ff51346591e189cd76c8518f7288bb1ea8336396259b']

    def test_hd2_status(self):
        path         = f"{self.prefix}/hd2/status"
        status_files = self.client.GET(path)
        assert len(status_files) == 1
        for file in status_files:
            assert file_exists(file)

    def test_hd3(self):
        num_of_files = 1
        path = f"{self.prefix}/hd3/{num_of_files}"
        files = self.client.GET(path)
        assert len(files) == num_of_files
        for file in files:
            assert file_exists(file)




