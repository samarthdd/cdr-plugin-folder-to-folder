import os
from urllib.parse import urljoin

from osbot_utils.utils.Http import GET_json,POST,POST_json


class Client:

    def __init__(self, url_server):
        self.server_ip = url_server

    # helper methods
    def _resolve_url(self, path=""):
        return urljoin(self.server_ip, path)

    def _request_get(self, path):
        url = self._resolve_url(path)
        return GET_json(url)

    def _request_post(self, path):
        url = self._resolve_url(path)
        return POST(url=url,data=b'', headers=None)

    # API methods
    def health(self):
        return self._request_get('/health')

    def version(self):
        return self._request_get('/version')

    def pre_process(self):
        return self._request_post('/pre-processor/pre-process')

    def start_process(self):
        return self._request_post('/processing/start')
