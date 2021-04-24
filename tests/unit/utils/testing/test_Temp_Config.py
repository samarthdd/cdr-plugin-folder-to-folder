from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import parent_folder, temp_folder_current

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing
from cdr_plugin_folder_to_folder.utils.testing.Temp_Config import Temp_Config


class test_Temp_Config(TestCase):

    def setUp(self) -> None:
        self.setup_testing = Setup_Testing()

    def test__setUpClass__tearDownClass(self):
        config          = Config()
        original_config = config.values()

        assert Temp_Config.setup_testing        is None
        assert Temp_Config.storage              is None
        assert Temp_Config.config               is None

        Temp_Config.setUpClass()
        assert type(Temp_Config.setup_testing)  is Setup_Testing
        assert type(Temp_Config.storage      )  is Storage
        assert type(Temp_Config.config       )  is Config
        assert parent_folder(config.root_folder) == temp_folder_current()
        assert original_config != config.values()

        Temp_Config.tearDownClass()
        assert Temp_Config.setup_testing        is None
        assert Temp_Config.storage              is None
        assert Temp_Config.config               is None

        self.setup_testing.configure_static_logging()
        assert original_config == config.values()