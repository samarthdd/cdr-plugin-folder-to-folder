from unittest import TestCase

from cdr_plugin_folder_to_folder.api.Server import Server


class test_Server(TestCase):

    def setUp(self) -> None:
        self.server = Server()

    def test_setup(self):
        self.server.setup()