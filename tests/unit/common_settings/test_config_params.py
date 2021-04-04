import os
from unittest import TestCase
from cdr_plugin_folder_to_folder.common_settings.config_params import *

class test_Config(TestCase):

    def setUp(self) -> None:
        self.config  = Config().load_values()

    def test_load_values(self):
        self.assertEqual(self.config.hd1_location   , os.environ.get("HD1_LOCATION"   , DEFAULT_HD1_LOCATION))
        self.assertEqual(self.config.hd2_location   , os.environ.get("HD2_LOCATION"   , DEFAULT_HD2_LOCATION))
        self.assertEqual(self.config.hd3_location   , os.environ.get("HD3_LOCATION"   , DEFAULT_HD3_LOCATION))
        self.assertEqual(self.config.gw_sdk_address , os.environ.get("GW_SDK_ADDRESS" , DEFAULT_GW_SDK_ADDRESS))
        self.assertEqual(self.config.gw_sdk_port    , int(os.environ.get("GW_SDK_PORT", DEFAULT_GW_SDK_PORT)))

