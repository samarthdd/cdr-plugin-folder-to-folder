from unittest import TestCase

from cdr_plugin_folder_to_folder.storage.Local_Storage import Local_Storage


class test_Local_Storage(TestCase):

    def setUp(self) -> None:
        self.local_storage = Local_Storage()

    def test_setup(self):
        # use case 1 - no values provided to setup
        self.local_storage.setup()
