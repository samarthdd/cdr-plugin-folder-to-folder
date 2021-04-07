from multiprocessing.context import Process
from unittest import TestCase
from unittest.mock import patch, call

from fastapi import FastAPI
from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.api.Server import Server
from cdr_plugin_folder_to_folder.utils.testing.Temp_API_Server import Temp_API_Server


class test_Server(TestCase):

    def setUp(self) -> None:
        app = FastAPI()
        self.server = Server(app=app, reload=False)

    def test_setup(self):
        self.server.setup()

    @patch("uvicorn.run")
    def test_start(self, mock_run):
        expected_call = call('cdr_plugin_folder_to_folder.api.Server:app',
                              host='0.0.0.0',
                              port=8880,
                              log_level='info',
                              reload=False)
        self.server.start()
        assert mock_run.mock_calls == [expected_call]

    def test_start_stop(self):
        with Temp_API_Server() as api_server:
            assert api_server.server_running() is True
            assert api_server.http_GET() == {'status': 'ok'}
        assert api_server.server_running() is False

    # def test_start(self):
    #     self.server.setup().start()
