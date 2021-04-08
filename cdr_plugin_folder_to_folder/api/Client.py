from urllib.parse import urljoin

from osbot_utils.utils.Http import GET_json


class Client:

    def __init__(self, url_server):
        self.server_ip = url_server

    # helper methods
    def _resolve_url(self, path=""):
        return urljoin(self.server_ip, path)

    def _request_get(self, path):
        url = self._resolve_url(path)
        return GET_json(url)

    # API methods
    def health(self):
        return self._request_get('/health')

    def version(self):
        return self._request_get('/version')

    # def file_distributor_hd1(self, num_of_files):
    #     path = f"/file-distributor/hd1/{num_of_files}"
    #     return self._request_get(path)