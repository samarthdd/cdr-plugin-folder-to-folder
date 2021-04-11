import json

import requests
from requests.auth import HTTPBasicAuth


class Kibana:
    def __init__(self, index_name=None, host=None, port=None, schema=None):
        self.index_name = index_name or 'test_index'
        self.host       = host or 'localhost'
        self.port       = port or '5601'
        self.schema     = schema or 'http'
        self.username   = None
        self.password   = None

    # helper methods

    def get_request_kwargs(self):
        headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'kibana'}
        kwargs = {"headers": headers}
        if self.username and self.password:
            kwargs['auth'] = HTTPBasicAuth(self.username, self.password)
        return kwargs

    def get_request(self, path):  # todo: add auth
        url = f'{self.schema}://{self.host}:{self.port}/{path}'
        kwargs = self.get_request_kwargs()

        response = requests.get(url, **kwargs)
        return json.loads(response.text)

    def post_request(self, path, payload):  # todo refactor out setup section (which will be same for all requests)
        data = json.dumps(payload)
        url = f'{self.schema}://{self.host}:{self.port}/{path}'
        kwargs = self.get_request_kwargs()

        response = requests.post(url, data, **kwargs)

        return json.loads(response.text)

    def kibana_api__find_saved_objects(self, type, fields, results_per_page=10000):
        """kibana api: https://www.elastic.co/guide/en/kibana/master/saved-objects-api-find.html
           todo: add support for more handling more than 10000 results
        """
        path = f'api/saved_objects/_find?fields={fields}&per_page={results_per_page}&type={type}'

        return self.get_request(path).get('saved_objects')

    # api methods

    def features(self):
        return self.get_request('api/features')