import json
from unittest import TestCase
from cdr_plugin_folder_to_folder.utils.testing.Direct_API_Server import Direct_API_Server
from os import environ

class test_Configure_Env(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Direct_API_Server().setup()
        cls.prefix = 'configaration'

    def test_configure(self):
        path = f"{self.prefix}/configure_env/"
        json_obj={
                      "hd1_path": "./test_data/scenario-1/hd1",
                      "hd2_path": "./test_data/scenario-1/hd2",
                      "hd3_path": "./test_data/scenario-1/hd3",
                      "gw_address": "127.0.0.1",
                      "gw_port": "8000"
                    }
        response = self.client.POST(
            path,
            json=json_obj,)
        assert response is not None
        assert response == json_obj

    def test_configure_multiple_gw_sdk_endpoints(self):
        path = f"{self.prefix}/configure_gw_sdk_endpoints/"
        endpoints = {'Endpoints': [{'IP': '0.0.0.0', 'Port': '8080'}, {'IP': '127.0.0.1', 'Port': '8080'}]}
        response = self.client.POST(
            path,
            json=endpoints
        )
        assert response is not None
        assert response == json.dumps(endpoints)











