import json

import requests
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Http import DELETE, GET
from requests.auth import HTTPBasicAuth


class For_Osbot_Elastic:

    def __init__(self, index=None, kibana=None, port=None, schema=None):
        self.index = index      or 'test_index'
        self.kibana = kibana    or 'localhost'
        self.port = port        or '5601'
        self.schema = schema    or 'http'
        self.username = None
        self.password = None

    # helper methods

    def get_request_kwargs(self):
        headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'kibana'}
        kwargs = { "headers": headers }
        if self.username and self.password:
            kwargs['auth'] = HTTPBasicAuth(self.username, self.password)
        return kwargs

    def get_request(self,path):                                     # todo: add auth
        url = f'{self.schema}://{self.kibana}:{self.port}/{path}'
        kwargs   = self.get_request_kwargs()

        response = requests.get(url, **kwargs)
        return json.loads(response.text)

    def post_request(self, path, payload):                          # todo refactor out setup section (which will be same for all requests)
        data     = json.dumps(payload)
        url      = f'{self.schema}://{self.kibana}:{self.port}/{path}'
        kwargs   = self.get_request_kwargs()

        response = requests.post(url, data, **kwargs)

        return json.loads(response.text)

    def kibana_api__find_saved_objects(self, type, fields, results_per_page=10000):
        """kibana api: https://www.elastic.co/guide/en/kibana/master/saved-objects-api-find.html
           todo: add support for more handling more than 10000 results
        """
        path = f'api/saved_objects/_find?fields={fields}&per_page={results_per_page}&type={type}'

        return self.get_request(path).get('saved_objects')

    # api methods

    def create_index_pattern(self, time_field = None):
        if time_field:
            payload = {"attributes":{"title": self.index ,"fields":"[]", f"timeFieldName": f"{time_field}"}}
        else:
            payload= {"attributes":{"title": self.index ,"fields":"[]"}}

        return self.post_request('api/saved_objects/index-pattern', payload)


    def delete_index_pattern(self):
        try:
            if self.host == 'localhost':
                url = f'{self.schema}://{self.host}:{self.port}/.kibana/doc/index-pattern:{self.index}'
                self._result = json.loads(DELETE(url))
            #else:
                #not working, will need to use something like /api/saved_objects/index-pattern/784b1a30-3931-11ea-a5e9-45b5e8966813
                #url = 'https://{0}:{1}/.kibana/doc/index-pattern:{2}'.format(self.host, self.port, self.index)
                #response = requests.delete(url, auth=HTTPBasicAuth(self.username, self.password))
                #self._result = json.loads(response.text)
        except Exception as error:
            self._result = { 'error':  error}
        return self

    def index_pattern(self, id=None, title=None):
        return 'test_index'
    @index_by
    @group_by
    def index_patterns(self):
        data = self.kibana_api__find_saved_objects('index-pattern', '*')
        results = []
        for item in data:                                                   # todo: see if this can be refactored into kibana_api__find_saved_objects
            result = {
                        "id": item.get('id'),
                        "namespaces": item.get('namespaces'),
                        "references": item.get('references'),
                     }
            result.update(item.get('attributes'))
            results.append(result)
        return results

        #return self.get_request('api/saved_objects/_find?fields=title&fields=type&per_page=10000&type=index-pattern')


