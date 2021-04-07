from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.api.Client import Client


class test_Client(TestCase):

    def setUp(self):
        #self.url_server = 'http://127.0.0.1:8880/'
        self.url_server = 'http://34.248.199.106:8880'
        self.client = Client(url_server=self.url_server)

    def test_health(self):
        result = self.client.health()
        assert result['status'] == 'ok'

    def test_file_distributor_hd1(self):
        num_of_files = 1
        result = self.client.file_distributor_hd1(num_of_files)
        pprint(result)

    #def test_version(self):
    #    result = self.client.version()
    #    assert result['version'] == 'v0.5'
