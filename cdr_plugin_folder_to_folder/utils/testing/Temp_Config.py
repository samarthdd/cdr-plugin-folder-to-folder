from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_delete
from osbot_utils.utils.Misc import random_text

from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.utils.Logging_Process import start_logging
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data


class Temp_Config(TestCase):
    config        = None
    log_worker    = None
    setup_testing = None
    storage       = None


    @classmethod
    def setUpClass(cls) -> None:
        cls.setup_testing = Setup_Testing()
        cls.log_worker    = start_logging()
        cls.storage       = Storage()
        cls.config        = cls.storage.config

        cls.setup_testing.set_config_to_temp_folder()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.setup_testing.restore_config()
        cls.setup_testing   = None
        cls.storage         = None
        cls.config          = None

    def add_test_files_h1(self, count=5, text_size=10):
        added_files = []
        for i in range(1, count+1):
            text = random_text(prefix=f"Random text with size {text_size}: ", length=text_size)
            test_file = Test_Data().create_test_pdf(text=text, file_key=f"temp_file_{i}")
            added_files.append(self.storage.hd1_add_file(test_file))
            file_delete(test_file)
        return added_files
