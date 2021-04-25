from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import json_to_str, json_parse

from cdr_plugin_folder_to_folder.configure.Configure_Env import Configure_Env


class test_Configure_Env(TestCase):

    def setUp(self):
        self.configure_env = Configure_Env()

    def test_get_valid_endpoints(self):
        test_ips =[   '54.216.215.247',
                      '3.250.105.142',
                      '52.211.122.246',
                      '34.244.186.10',
                      '54.170.169.208',
                      '63.32.93.141',
                      '34.247.81.39']
        endpoints = []
        for ip in test_ips:
            endpoints.append({'IP': ip, "Port": "8080"})

        valid_endpoints = {'Endpoints' : endpoints }
        endpoint_string = json_to_str(valid_endpoints)
        result = self.configure_env.get_valid_endpoints(endpoint_string)
        pprint(json_parse(result))


