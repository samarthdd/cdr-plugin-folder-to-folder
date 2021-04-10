from unittest import TestCase
from cdr_plugin_folder_to_folder.configure.Configure_Env import Configure_Env
from os import environ
from dotenv import load_dotenv
class test_Configure_Env(TestCase):

    def setUp(self) -> None:
        self.configure = Configure_Env()
        load_dotenv()

    def test_configure(self):
        hd1_path      = "./test_data/scenario-1/hd1"
        hd2_path      = "./test_data/scenario-1/hd2"
        hd3_path      = "./test_data/scenario-1/hd3"
        gw_address    = "127.0.0.1"
        gw_port       = "8000"

        response=self.configure.configure(hd1_path=hd1_path,
                                          hd2_path=hd2_path,
                                          hd3_path=hd3_path,
                                          gw_address=gw_address,
                                          gw_port=gw_port)

        assert response is not None
        self.assertEqual(environ["HD1_LOCATION"]   , hd1_path)
        self.assertEqual(environ["HD2_LOCATION"]   , hd2_path)
        self.assertEqual(environ["HD3_LOCATION"]   , hd3_path)
        self.assertEqual(environ["GW_SDK_ADDRESS"] , gw_address)
        self.assertEqual(environ["GW_SDK_PORT"]    , gw_port)

    def test_configure_multiple_gw_sdk_endpoints(self):
        endpoint_string='{"Endpoints":[{"IP":"0.0.0.0", "Port":"8080"},{"IP":"0.0.0.1", "Port":"8080"}]}'
        response=self.configure.configure_endpoints(endpoint_string=endpoint_string)
        assert response is not None
        self.assertEqual(response   , endpoint_string)





