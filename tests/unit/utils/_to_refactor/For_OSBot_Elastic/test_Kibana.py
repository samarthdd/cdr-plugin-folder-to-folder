from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana import Kibana


class test_Kibana(TestCase):

    def setUp(self) -> None:
        self.config     = Config().load_values()
        self.host       = self.config.kibana_host
        self.port       = self.config.kibana_port
        self.index_name = 'temp_index'
        self.kibana     = Kibana(index_name=self.index_name, host=self.host, port=self.port)

    def test_features(self):
        pprint(self.kibana.features())

