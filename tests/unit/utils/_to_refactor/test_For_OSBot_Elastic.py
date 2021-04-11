from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.utils._to_refactor.For_Osbot_Elastic import For_Osbot_Elastic


class test_For_OSBot_Elastic(TestCase):

    def setUp(self) -> None:
        self.index_name = 'temp_index_pattern'
        self.osbot_elastic = For_Osbot_Elastic()

    def test_index_patters(self):
        pprint(self.osbot_elastic.index_patterns())

    def test_create_index_pattern(self):
        #result = self.osbot_elastic.create_index_pattern()
        pprint(result)
