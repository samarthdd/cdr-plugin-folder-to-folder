import os
from unittest import TestCase

from cdr_plugin_folder_to_folder.common_settings.config_params import Config


class test_Config(TestCase):

    def setUp(self) -> None:
        self.config  = Config()

    def test_config(self):
        # todo: bug, test_data/h2 is created in the test folder
        self.assertEqual(self.config.hd1_location   , os.environ.get("HD1_LOCATION"))
        self.assertEqual(self.config.hd2_location   , os.environ.get("HD2_LOCATION"))
        self.assertEqual(self.config.hd3_location   , os.environ.get("HD3_LOCATION"))
        self.assertEqual(self.config.gw_sdk_address , os.environ.get("GW_SDK_ADDRESS"))
        self.assertEqual(self.config.gw_sdk_port    , int(os.environ.get("GW_SDK_PORT")))
        assert os.path.exists(self.config.temp_folder   )  is True
        assert os.path.exists(self.config.data_folder   )  is True
        assert os.path.exists(self.config.status_folder )  is True

