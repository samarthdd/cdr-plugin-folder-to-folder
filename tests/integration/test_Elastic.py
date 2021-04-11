from os import environ
from unittest import TestCase

import pytest
from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.utils.Elastic import Elastic


class test_Elastic(TestCase):

    def setUp(self) -> None:
        self.elastic = Elastic()
        if self.elastic.server_online() is False:
            pytest.skip('Elastic server not available')

    def test_elastic(self):
        assert len(self.elastic.elastic().index_list()) > 0

    def test_add(self):
        data = { "more":"data"}
        self.elastic.add(data)

    def test_setup(self):
        self.elastic.setup()
        assert self.elastic.index().exists()
        assert self.elastic.index_pattern().exists()

    def test_server_online(self):
        assert self.elastic.server_online() is True
        self.elastic.config.elastic_port='9201'
        assert self.elastic.server_online() is False
