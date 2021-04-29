from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import json_to_str, json_parse

from cdr_plugin_folder_to_folder.configure.Configure_Env import Configure_Env


class test_Configure_Env(TestCase):

    def setUp(self):
        self.configure_env = Configure_Env()

    def test_get_valid_endpoints(self):
#        test_ips =[   '3.250.55.150',
#                      '34.242.205.32',
#                      '3.250.152.58',
#                      '3.248.208.74',
#                      '54.195.161.214',
#                      '54.75.120.78',
#                      '3.250.212.118']

        test_ips =[   '3.250.175.87' ]

        endpoints = []
        for ip in test_ips:
            endpoints.append({'IP': ip, "Port": "8080"})

        valid_endpoints = {'Endpoints' : endpoints }
        endpoint_string = json_to_str(valid_endpoints)
        result = self.configure_env.get_valid_endpoints(endpoint_string)
        responsive_endpoints = json_parse(result).get('Endpoints')
        assert len(responsive_endpoints) > 0
        for enpoint in responsive_endpoints:
            assert enpoint in endpoints


