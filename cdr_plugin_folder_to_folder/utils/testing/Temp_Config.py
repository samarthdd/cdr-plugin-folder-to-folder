from unittest import TestCase

from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing

class Temp_Config(TestCase):
    setup_testing = None
    storage       = None
    config        = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.setup_testing = Setup_Testing()
        cls.storage       = Storage()
        cls.config        = cls.storage.config

        cls.setup_testing.set_config_to_temp_folder()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.setup_testing.restore_config()
        cls.setup_testing   = None
        cls.storage         = None
        cls.config          = None