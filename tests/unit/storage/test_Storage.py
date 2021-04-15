from os.path import abspath
from unittest import TestCase

from osbot_utils.utils.Files import path_combine

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.storage.Storage import Storage


class test_Storage(TestCase):

    def setUp(self) -> None:
        self.config        = Config()
        self.local_storage = Storage()

    def test_hd1_hd2_hd3(self):
        assert self.local_storage.hd1() == abspath(self.config.hd1_location)
        assert self.local_storage.hd2() == abspath(self.config.hd2_location)
        assert self.local_storage.hd3() == abspath(self.config.hd3_location)