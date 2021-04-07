from unittest import TestCase

from fastapi import FastAPI

from cdr_plugin_folder_to_folder.api.Server import Server


class test_Server(TestCase):

    def setUp(self) -> None:
        app = FastAPI()
        self.server = Server(app=app)

    def test_setup(self):
        self.server.setup()

    # def test_start(self):
    #     self.server.setup().start()
