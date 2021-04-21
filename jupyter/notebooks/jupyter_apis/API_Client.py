import os
from urllib.parse import urljoin
import requests
import json
from osbot_utils.utils.Http import GET_json, POST, POST_json
from osbot_utils.utils.Json import str_to_json, json_to_str

DEFAULT_API_SERVER = 'http://api:8880'


class API_Client:

    def __init__(self, url_server=DEFAULT_API_SERVER):
        self.server_ip = url_server

    # helper methods
    def _resolve_url(self, path=""):
        return urljoin(self.server_ip, path)

    def _request_get(self, path):
        url = self._resolve_url(path)
        return GET_json(url)

    def _request_post(self, path):
        url = self._resolve_url(path)
        return POST(url=url, data=b'', headers=None)

    def _request_http_post(self, path, data, headers):
        url = self._resolve_url(path)
        return requests.post(url=url, data=data, headers=headers)

    # API methods
    def clear_data_and_status(self):
        return self._request_post('/pre-processor/clear-data-and-status')

    def health(self):
        return self._request_get('/health')

    def version(self):
        return self._request_get('/version')

    def pre_process(self):
        return self._request_post('/pre-processor/pre-process')

    def process_files(self):
        assert self.pre_process() == '["Processing is done"]'
        assert self.start_process() == '"Loop completed"'

        return "all files processed "

    def start_process(self):
        return self._request_post('/processing/start')

    def stop_process(self):
        return self._request_post('/processing/stop')

    def configure_environment(self, data):
        headers = {'accept': 'application/json',
                   'Content-Type': 'application/json'}
        post_data = json_to_str(data)
        return self._request_http_post(path="configuration/configure_env", headers=headers, data=post_data)

    def set_gw_sdk_endpoints(self, data):
        headers = {'accept': 'application/json',
                   'Content-Type': 'application/json'}
        post_data = json_to_str(data)
        return self._request_http_post(path="configuration/configure_gw_sdk_endpoints", headers=headers, data=post_data)

    # helper methods

    def configure(self, data_paths, sdk_endpoints, clear_data=False):
        status = {}
        if clear_data:
            status['clear_data_and_status'] = self.clear_data_and_status()
        status['configure_environment'] = self.configure_environment(data=data_paths)
        status['set_gw_sdk_endpoints'] = self.set_gw_sdk_endpoints(data=sdk_endpoints)
        return status

    def get_processing_status(self):
        return self._request_get('/processing/status')