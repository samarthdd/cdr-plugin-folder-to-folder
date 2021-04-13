import json
from unittest import TestCase

import pytest

from cdr_plugin_folder_to_folder.configure.Configure_Env import Configure_Env
from os import environ,path,remove
from dotenv import load_dotenv
class test_Configure_Env(TestCase):

    def setUp(self) -> None:
        self.configure = Configure_Env()
        load_dotenv()

    @pytest.mark.skip("this is breaking current .env file (this needs to run on a temp .env file)")
    def test_configure(self):
        hd1_path      = "./test_data/scenario-1/hd1"
        hd2_path      = "./test_data/scenario-1/hd2"
        hd3_path      = "./test_data/scenario-1/hd3"

        response=self.configure.configure(hd1_path=hd1_path,
                                          hd2_path=hd2_path,
                                          hd3_path=hd3_path)

        assert response is not None
        self.assertEqual(environ["HD1_LOCATION"]   , hd1_path)
        self.assertEqual(environ["HD2_LOCATION"]   , hd2_path)
        self.assertEqual(environ["HD3_LOCATION"]   , hd3_path)

    @pytest.mark.skip("this is breaking current .env file (this needs to run on a temp .env file)")
    def test_configure_multiple_gw_sdk_endpoints(self):
        endpoint_string='{"Endpoints":[{"IP":"0.0.0.0", "Port":"8080"},{"IP":"0.0.0.1", "Port":"8080"}]}'
        response=self.configure.configure_endpoints(endpoint_string=endpoint_string)
        assert response is not None
        self.assertEqual(response   , json.loads(endpoint_string))





