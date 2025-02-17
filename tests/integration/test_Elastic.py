from os import environ
from unittest import TestCase

import pytest
from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.utils.Elastic import Elastic
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing


class test_Elastic(TestCase):

    def setUp(self) -> None:
        Setup_Testing().pytest_skip_if_elastic_not_available()
        self.elastic = Elastic().setup()
        #Setup_Testing().configure_elastic(elastic=self.elastic)
        #if self.elastic.enabled is False:
        #    pytest.skip('Elastic server not available')

    def test_elastic(self):
        assert len(self.elastic.elastic().index_list()) > 0

    def test_add(self):
        data = { "more":"data"}
        self.elastic.add(data)

    def test_create_index_and_index_pattern(self):
        self.elastic.create_index_and_index_pattern()
        assert self.elastic.index().exists()
        assert self.elastic.index_pattern().exists()

    def test_server_online(self):
        assert self.elastic.server_online() is True
        self.elastic.config.elastic_port='9201'
        assert self.elastic.server_online() is False
        self.elastic.config.elastic_port = '9200'                   # need to restore this value since we are modifying an singleton object
        assert self.elastic.server_online() is True
