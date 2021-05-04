from unittest import TestCase

import pytest
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import json_save_file, json_load_file
from osbot_utils.utils.Misc import list_set

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.utils.Elastic import Elastic
from cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana import Kibana

#@pytest.mark.skip
# todo create a number of test objects in setUpClass (so that asserts have data to test against)
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing


class test_Kibana(TestCase):

    def setUp(self) -> None:
        self.config = Config()
        Setup_Testing().configure_config(self.config)

        self.host       = self.config.kibana_host
        self.port       = self.config.kibana_port
        self.index_name = 'temp_index'
        self.kibana     = Kibana(index_name=self.index_name, host=self.host, port=self.port)

        self.kibana.setup()
        if self.kibana.enabled is False:
            pytest.skip('Kibana server not available')

    def test_dashboards(self):
        dashboards   = json_load_file('/var/folders/_j/frqs70d93l328f307rw2jx5h0000gn/T/tmp628dz7n_.tmp')
        dashboard    = dashboards[0]
        dashboard_id = dashboard.get('id')
        pprint(dashboard)
        #results = self.kibana.dashboards()
        #pprint(json_save_file(results))

    def test_features(self):
        features                = self.kibana.features(index_by='id')
        index_patterns_features = features.get('indexPatterns')

        assert len(features) > 5
        assert index_patterns_features.get('app') == ['kibana']

    def test_index_patterns(self):
        results = self.kibana.index_patterns()
        #
        # pprint(results)
        # if len(results) > 0:
        #     assert list_set(results.pop()) == ['fields', 'id', 'namespaces', 'references', 'title']

    def test_visualisations(self):
        results = self.kibana.visualizations()
        #pprint(results)

    def test_server_online(self):
        pprint(self.kibana.server_online())