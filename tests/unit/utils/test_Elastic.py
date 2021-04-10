from os import environ
from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.utils.Elastic import Elastic


class test_Elastic(TestCase):

    def setUp(self) -> None:
        self.elastic = Elastic()

    def test_elastic(self):
        assert len(self.elastic.elastic().index_list()) > 0

    def test_add(self):
        data = { "more":"data"}
        self.elastic.add(data)

    def test_setup(self):
        self.elastic.setup()
        pprint(self.elastic.elastic())

