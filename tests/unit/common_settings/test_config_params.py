import os
import json
from unittest import TestCase

from osbot_utils.utils.Files import folder_exists

from cdr_plugin_folder_to_folder.common_settings.Config import *

class test_Config(TestCase):

    def setUp(self) -> None:
        self.config  = Config().load_values()

    def test_load_values(self):
        self.assertEqual(self.config.gw_sdk_address , os.environ.get("GW_SDK_ADDRESS" , DEFAULT_GW_SDK_ADDRESS))
        self.assertEqual(self.config.gw_sdk_port    , int(os.environ.get("GW_SDK_PORT", DEFAULT_GW_SDK_PORT)))
        self.assertEqual(self.config.hd1_location   , os.environ.get("HD1_LOCATION"   , DEFAULT_HD1_LOCATION))
        self.assertEqual(self.config.hd2_location   , os.environ.get("HD2_LOCATION"   , DEFAULT_HD2_LOCATION))
        self.assertEqual(self.config.hd3_location   , os.environ.get("HD3_LOCATION"   , DEFAULT_HD3_LOCATION))
        self.assertEqual(self.config.root_folder    , os.environ.get("ROOT_FOLDER"    , DEFAULT_ROOT_FOLDER))
        self.assertEqual(self.config.endpoints      , json.loads(os.environ.get("ENDPOINTS"      , DEFAULT_ENDPOINTS)))
        assert self.config.endpoints['Endpoints'][0]['IP']
        assert self.config.endpoints['Endpoints'][0]['Port']

        assert folder_exists(self.config.root_folder )
        assert folder_exists(self.config.hd1_location)
        assert folder_exists(self.config.hd2_location)
        assert folder_exists(self.config.hd3_location)

