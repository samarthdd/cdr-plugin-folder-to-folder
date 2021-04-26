from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, path_combine, temp_folder, temp_folder_current, parent_folder, \
    folder_not_exists

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing


class test_Setup_Testing(TestCase):
    def setUp(self) -> None:
        self.setup_testing = Setup_Testing()

    def test_path_repo_root(self):
        path_repo = self.setup_testing.path_repo_root()
        assert folder_exists(path_repo)
        assert folder_exists(path_combine(path_repo, '.git'))
        assert folder_exists(path_combine(path_repo, 'test_data'))

    def test_set_test_root_dir(self):
        self.setup_testing.set_test_root_dir()
        assert folder_exists(path_combine('.', '.git'))
        assert folder_exists(path_combine('.', 'test_data'))

    def test_set_config_to_temp_folder__restore_config(self):
        storage         = Storage()
        config          = storage.config
        original_config = config.values()
        self.setup_testing.set_config_to_temp_folder()
        temp_config     = config.values()

        assert parent_folder(config.root_folder  ) == temp_folder_current()
        assert folder_exists(config.root_folder  )
        assert folder_exists(storage.hd1()       )
        assert folder_exists(storage.hd2_status())
        assert folder_exists(storage.hd2_data()  )
        assert folder_exists(storage.hd3()       )
        assert original_config != temp_config

        self.setup_testing.restore_config()
        #self.setup_testing.configure_static_logging()
        assert original_config == config.values()
        assert parent_folder(config.root_folder) != temp_folder_current()
        assert folder_not_exists(temp_config.get('root_folder'))
