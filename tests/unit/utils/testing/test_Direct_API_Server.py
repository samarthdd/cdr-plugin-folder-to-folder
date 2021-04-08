from unittest import TestCase

import pytest
from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.utils.testing.Direct_API_Server import Direct_API_Server


#@pytest.mark.skip
class test_Direct_API_Server(TestCase):
    def setUp(self) -> None:
        self.client = Direct_API_Server().setup()

    def test_GET(self):
        assert self.client.GET('/health') == {'status': 'ok'}

    # def test__enter__(self):
    #     with Direct_API_Server() as server:
    #         assert server.GET('/health') == {'status': 'ok'}
