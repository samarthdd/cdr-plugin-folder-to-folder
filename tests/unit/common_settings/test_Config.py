from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists
from osbot_utils.utils.Misc import list_set

from cdr_plugin_folder_to_folder.common_settings.Config import *

class test_Config(TestCase):

    def setUp(self) -> None:
        self.config  = Config()

    def test_load_values(self):
        assert Config.config_cache == self.config
        config = self.config

        self.assertEqual(config.gw_sdk_address , os.environ.get("GW_SDK_ADDRESS" , DEFAULT_GW_SDK_ADDRESS))
        self.assertEqual(config.gw_sdk_port    , int(os.environ.get("GW_SDK_PORT", DEFAULT_GW_SDK_PORT)))
        self.assertEqual(config.hd1_location   , os.environ.get("HD1_LOCATION"   , DEFAULT_HD1_LOCATION))
        self.assertEqual(config.hd2_location   , os.environ.get("HD2_LOCATION"   , DEFAULT_HD2_LOCATION))
        self.assertEqual(config.hd3_location   , os.environ.get("HD3_LOCATION"   , DEFAULT_HD3_LOCATION))
        self.assertEqual(config.root_folder    , os.environ.get("ROOT_FOLDER"    , DEFAULT_ROOT_FOLDER))
        self.assertEqual(config.endpoints      , json.loads(os.environ.get("ENDPOINTS"      , DEFAULT_ENDPOINTS)))
        assert config.endpoints['Endpoints'][0]['IP']
        assert config.endpoints['Endpoints'][0]['Port']

        assert folder_exists(config.root_folder )
        assert folder_exists(config.hd1_location)
        assert folder_exists(config.hd2_location)
        assert folder_exists(config.hd3_location)

        # check config_cache
        config.root_folder = 'aaa'
        config.load_values()
        assert config.root_folder == 'aaa'
        config.load_values(reload=True)
        assert config.root_folder == DEFAULT_ROOT_FOLDER



    def test_set_root_folder(self):
        root_folder = temp_folder()
        assert self.config.root_folder != root_folder
        self.config.set_root_folder(root_folder)
        assert self.config.root_folder  == root_folder

        assert self.config.hd1_location == path_combine(root_folder, DEFAULT_HD1_NAME)
        assert self.config.hd2_location == path_combine(root_folder, DEFAULT_HD2_NAME)
        assert self.config.hd3_location == path_combine(root_folder, DEFAULT_HD3_NAME)

        assert folder_exists(self.config.root_folder )
        assert folder_exists(self.config.hd1_location)
        assert folder_exists(self.config.hd2_location)
        assert folder_exists(self.config.hd3_location)

        
        assert self

    def test_get_values(self):
        values = self.config.values()
        assert self.config.values().get('root_folder') == self.config.root_folder
        assert list_set(values) == ['elastic_host', 'elastic_port', 'elastic_schema', 'endpoints', 'gw_sdk_address', 'gw_sdk_port', 'hd1_location', 'hd2_location', 'hd3_location', 'kibana_host', 'kibana_port', 'root_folder', 'thread_count']
