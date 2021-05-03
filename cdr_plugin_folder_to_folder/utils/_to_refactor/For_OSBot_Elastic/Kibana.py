import json

import requests
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Files import file_copy
from osbot_utils.utils.Http import GET
from requests.auth import HTTPBasicAuth

from cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Dashboard import Dashboard


class Kibana:
    def __init__(self, index_name=None, host=None, port=None, schema=None):
        self.index_name = index_name    or 'test_index'
        self.host       = host          or 'localhost'
        self.port       = port          or '5601'
        self.schema     = schema        or 'http'
        self.username   = None
        self.password   = None
        self.enabled    = False

    # helper methods
    # todo refactor these methods to the schema: request_{METHOD}
    def get_request_kwargs(self):
        headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'kibana'}
        kwargs  = {"headers": headers}
        if self.username and self.password:
            kwargs['auth'] = HTTPBasicAuth(self.username, self.password)
        return kwargs

    def delete_request(self, path):
        if self.enabled:
            url      = self.request_url(path)
            kwargs   = self.get_request_kwargs()
            response = requests.delete(url, **kwargs)
            return json.loads(response.text)

    def get_request(self, path):
        print()
        print(path)
        if self.enabled:
            url      = self.request_url(path)
            kwargs   = self.get_request_kwargs()
            response = requests.get(url, **kwargs)
            return json.loads(response.text)

    def post_request(self, path, payload, parse_into_json=True):  # todo refactor out setup section (which will be same for all requests)
        if self.enabled:
            data     = json.dumps(payload)
            url      = self.request_url(path)
            kwargs   = self.get_request_kwargs()
            response = requests.post(url, data, **kwargs)
            if parse_into_json:
                return json.loads(response.text)
            return response.text

    def post_file(self, path, path_file, parse_into_json=True):  # todo refactor out setup section (which will be same for all requests)
        if self.enabled:
            #ndjson_file = path_file + '.ndjson'
            #file_copy(path_file, ndjson_file)
            url      = self.request_url(path)
            #kwargs   = self.get_request_kwargs()
            kwargs = { 'headers' : {'kbn-xsrf': 'kibana'}} #'Content-Type': "multipart/form-data",
            files    = {'file': open(path_file , 'rb')}
            response = requests.post(url, files=files, **kwargs)
            if parse_into_json:
                return json.loads(response.text)
            return response.text

    def request_url(self, path):
        return f'{self.schema}://{self.host}:{self.port}/{path}'

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
        if kibana_objects:
            for kibana_object in kibana_objects:
                results.append(self.parse_kibana_object(kibana_object))
        return results

    def server_online(self):
        try:
            root_http = GET(self.request_url('/'))          # check that we can reach the server ok
            assert root_http.find('kibana') > 0             #
            self.enabled = True                             # if all is good, set the enabled flag
        except:
            return False

    def setup(self):
        self.server_online()
        return self
    # api methods

    @index_by
    def dashboards(self):
        return self.find("dashboard")

    def dashboard_import_from_github(self, dashboard_file_name):
        dashboard = Dashboard(kibana=self)
        return dashboard.import_dashboard_from_github(dashboard_file_name)

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
        result          = self.get_request(path)
        if result:
            kibana_objects = result.get('saved_objects')
            return self.parse_kibana_objects(kibana_objects)
        return {}


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
