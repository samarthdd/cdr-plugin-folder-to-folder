from unittest import TestCase

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.storage.Local_Storage import Local_Storage


class test_Local_Storage(TestCase):

    def setUp(self) -> None:
        self.config        = Config()
        self.local_storage = Local_Storage()

    def test_hd1_hd2_hd3(self):
        assert self.local_storage.hd1() == self.config.hd1_location
        assert self.local_storage.hd2() == self.config.hd2_location
        assert self.local_storage.hd3() == self.config.hd3_location