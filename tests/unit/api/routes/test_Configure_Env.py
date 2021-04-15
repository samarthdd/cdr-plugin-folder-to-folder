import json
from unittest import TestCase
from unittest.mock import patch

import pytest
import dotenv
from cdr_plugin_folder_to_folder.utils.testing.Direct_API_Server import Direct_API_Server
from os import environ,path,rename

class test_Configure_Env(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Direct_API_Server().setup()
        cls.prefix = 'configuration'
        cls._dotenv_file=dotenv.find_dotenv()
        if cls._dotenv_file :
            rename(cls._dotenv_file ,path.join(path.dirname(cls._dotenv_file),".env_backup"))

    @classmethod
    def tearDownClass(cls) -> None:
        if cls._dotenv_file:
            rename(path.join(path.dirname(cls._dotenv_file), ".env_backup"),cls._dotenv_file)

    def test_configure(self):
        path = f"{self.prefix}/configure_env/"
        json_obj={
                      "hd1_path": "./test_data/scenario-1/hd1",
                      "hd2_path": "./test_data/scenario-1/hd2",
                      "hd3_path": "./test_data/scenario-1/hd3"
                    }
        response = self.client.POST(
            path,
            json=json_obj,)
        assert response is not None
        assert response == json_obj

#    @pytest.mark.skip("this is breaking current .env file (this needs to run on a temp .env file)")
    @patch("cdr_plugin_folder_to_folder.configure.Configure_Env.Configure_Env.get_valid_endpoints")
    def test_configure_multiple_gw_sdk_endpoints(self,mock_get_valid_endpoints):
        path = f"{self.prefix}/configure_gw_sdk_endpoints/"
        expected_return_value = '{"Endpoints":[{"IP":"0.0.0.0", "Port":"8080"}]}'
        mock_get_valid_endpoints.return_value = expected_return_value
        endpoints = {'Endpoints': [{'IP': '0.0.0.0', 'Port': '8080'}, {'IP': '127.0.0.1', 'Port': '8080'}]}
        response = self.client.POST(
            path,
            json=endpoints
        )
        assert response is not None
        assert response == json.loads(mock_get_valid_endpoints)