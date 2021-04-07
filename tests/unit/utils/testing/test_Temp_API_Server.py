from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.utils.testing.Temp_API_Server import Temp_API_Server, run_server


class test_Temp_API_Server(TestCase):

    def setUp(self) -> None:
        self.api_server = Temp_API_Server()
        self.port       = self.api_server.port

    def test___init__(self):
        assert 20000 < self.port < 65000
        assert self.api_server.proc is None

    @patch("cdr_plugin_folder_to_folder.api.Server.Server.start")
    def test_server(self, mock_setup):
        run_server(port = self.port)
        #pprint(dir(mock_setup))
        assert mock_setup.mock_calls == [call()]


    def test_start_stop_GET(self):
        assert self.api_server.start_server()     == {'status': 'ok'}
        assert self.api_server.http_GET('health') == {'status': 'ok'}
        assert self.api_server.server_running()   is True
        self.api_server.stop_server()
        assert self.api_server.server_running()   is False

    def test_server_url(self):
        assert self.api_server.server_url() == f"http://127.0.0.1:{self.api_server.port}"

