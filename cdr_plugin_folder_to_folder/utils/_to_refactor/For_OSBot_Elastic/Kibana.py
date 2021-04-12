import json

import requests
from osbot_utils.decorators.lists.index_by import index_by
from requests.auth import HTTPBasicAuth


class Kibana:
    def __init__(self, index_name=None, host=None, port=None, schema=None):
        self.index_name = index_name    or 'test_index'
        self.host       = host          or 'localhost'
        self.port       = port          or '5601'
        self.schema     = schema        or 'http'
        self.username   = None
        self.password   = None

    # helper methods

    def delete_request(self, path):
        url = f'{self.schema}://{self.host}:{self.port}/{path}'
        kwargs = self.get_request_kwargs()

        response = requests.delete(url, **kwargs)
        return json.loads(response.text)

    def get_request_kwargs(self):
        headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'kibana'}
        kwargs = {"headers": headers}
        if self.username and self.password:
            kwargs['auth'] = HTTPBasicAuth(self.username, self.password)
        return kwargs

    def get_request(self, path):
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

    def parse_kibana_object(self, kibana_object):
        result = {  "id"        : kibana_object.get('id'        ),
                    "namespaces": kibana_object.get('namespaces'),
                    "updated_at": kibana_object.get('updated_at'),
                    "references": kibana_object.get('references'),
                    "score"     : kibana_object.get('score'     ),
                    "type"      : kibana_object.get('type'      )
            }
        result.update(kibana_object.get('attributes'))
        return result

    def parse_kibana_objects(self, kibana_objects):
        results = []
        for kibana_object in kibana_objects:
            results.append(self.parse_kibana_object(kibana_object))
        return results

    # api methods

    @index_by
    def dashboards(self):
        return self.find("dashboards")

    @index_by
    def features(self):
        return self.get_request('api/features')

    @index_by
    def find(self, object_type, search_query='*', search_fields='*', results_per_page=10000):
        """kibana api: https://www.elastic.co/guide/en/kibana/master/saved-objects-api-find.html
           todo: add support for more handling more than 10000 results
           type: visualization, dashboard, search, index-pattern, config, and timelion-sheet
        """
        path            = f"api/saved_objects/_find?type={object_type}&search_fields={search_fields}&search={search_query}&per_page={results_per_page}"
        kibana_objects  = self.get_request(path).get('saved_objects')
        return self.parse_kibana_objects(kibana_objects)


    @index_by
    def index_patterns(self):
        return self.find("index-pattern")

    def saved_objects(self):
        # https://www.elastic.co/guide/en/kibana/master/saved-objects-api-get.html
        # visualization, dashboard, search, index-pattern, config, and timelion-sheet.
        # /api/saved_objects/<type>/<id>

        pass

    def saved_objects_bulk(self):
        #https://www.elastic.co/guide/en/kibana/master/saved-objects-api-bulk-get.html
        pass

    def visualizations(self):
        return self.find("visualization")
