from unittest import TestCase


from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists

from cdr_plugin_folder_to_folder.common_settings.Config import API_VERSION
from cdr_plugin_folder_to_folder.utils.testing.Direct_API_Server import Direct_API_Server


class test_Health(TestCase):

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
        #assert self.client.GET("/health") == {'status': 'ok'}

