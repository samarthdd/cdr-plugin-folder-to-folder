import os
import json
from dotenv import load_dotenv
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_not_exists, path_combine, folder_create, create_folder, temp_folder, \
    folder_exists

# todo: refactor the whole test files so that it all comes from temp folders (not from files in the repo)

from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing

DEFAULT_HD1_NAME         = 'hd1'
DEFAULT_HD2_NAME         = 'hd2'
DEFAULT_HD3_NAME         = 'hd3'
DEFAULT_HD2_DATA_NAME    = 'data'
DEFAULT_HD2_STATUS_NAME  = 'status'
DEFAULT_ROOT_FOLDER      = path_combine(__file__                , '../../../test_data/scenario-1' )
DEFAULT_HD1_LOCATION     = path_combine(DEFAULT_ROOT_FOLDER     , DEFAULT_HD1_NAME                )
DEFAULT_HD2_LOCATION     = path_combine(DEFAULT_ROOT_FOLDER     , DEFAULT_HD2_NAME                )
DEFAULT_HD3_LOCATION     = path_combine(DEFAULT_ROOT_FOLDER     , DEFAULT_HD3_NAME                )
DEFAULT_ELASTIC_HOST     = "es01"
DEFAULT_ELASTIC_PORT     = "9200"
DEFAULT_ELASTIC_SCHEMA   = "http"
DEFAULT_KIBANA_HOST      = "kib01"
DEFAULT_KIBANA_PORT      = "5601"
DEFAULT_THREAD_COUNT     = 10
DEFAULT_TEST_SDK         = '84.16.229.232'
DEFAULT_ENDPOINTS        = '{"Endpoints":[{"IP":"' + DEFAULT_TEST_SDK + '", "Port":"8080"}]}'
DEFAULT_REQUEST_TIMEOUT  = 60
API_VERSION              = "v0.5.57"



class Config:
    _instance = None
    def __new__(cls):                                               # singleton pattern
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'root_folder') is False:                     # only set these values first time around
            self.hd1_location        = None
            self.hd2_location        = None
            self.hd2_data_location   = None
            self.hd2_status_location = None
            self.hd3_location        = None
            self.root_folder         = None
            self.elastic_host        = None
            self.elastic_port        = None
            self.elastic_schema      = None
            self.kibana_host         = None
            self.kibana_port         = None
            self.thread_count        = None
            self.test_sdk            = None
            self.endpoints           = None
            self.endpoints_count     = None
            self.request_timeout     = None
            self.load_values()                                      # due to the singleton pattern this will only be executed once

    def load_values(self):
        Setup_Testing().set_test_root_dir()                         # todo: fix test data so that we don't need to do this here
        load_dotenv(override=True)                                  # Load configuration from .env file that should exist in the root of the repo
        self.root_folder         = os.getenv    ("ROOT_FOLDER"     , DEFAULT_ROOT_FOLDER    )
        self.elastic_host        = os.getenv    ("ELASTIC_HOST"    , DEFAULT_ELASTIC_HOST   )
        self.elastic_port        = os.getenv    ("ELASTIC_PORT"    , DEFAULT_ELASTIC_PORT   )
        self.elastic_schema      = os.getenv    ("ELASTIC_SCHEMA"  , DEFAULT_ELASTIC_SCHEMA )
        self.kibana_host         = os.getenv    ("KIBANA_HOST"     , DEFAULT_KIBANA_HOST    )
        self.kibana_port         = os.getenv    ("KIBANA_PORT"     , DEFAULT_KIBANA_PORT    )
        self.thread_count        = os.getenv    ("THREAD_COUNT"    , DEFAULT_THREAD_COUNT   )
        self.request_timeout     = os.getenv    ("REQUEST_TIMEOUT" , DEFAULT_REQUEST_TIMEOUT)
        self.test_sdk            = os.getenv    ("DEFAULT_TEST_SDK", DEFAULT_TEST_SDK       )

        json_string          = os.getenv("ENDPOINTS", DEFAULT_ENDPOINTS)
        self.endpoints       = json.loads(json_string)

        self.endpoints_count = len(self.endpoints['Endpoints'])

        self.set_hd1_location(os.getenv("HD1_LOCATION", DEFAULT_HD1_LOCATION))       # set hd1, hd2 and hd3 values
        self.set_hd2_location(os.getenv("HD2_LOCATION", DEFAULT_HD2_LOCATION))
        self.set_hd3_location(os.getenv("HD3_LOCATION", DEFAULT_HD3_LOCATION))
        #pprint(self.values())
        return self

    def ensure_last_char_is_not_forward_slash(self, path: str):
        if path.endswith('/') or path.endswith('\\'):
            path = path[:-1]
        return path

    def set_hd1_location(self, hd1_location):
        self.hd1_location = self.ensure_last_char_is_not_forward_slash(hd1_location)
        folder_create(self.hd1_location)

    def set_hd2_location(self, hd2_location):
        self.hd2_location        = self.ensure_last_char_is_not_forward_slash(hd2_location)
        self.hd2_data_location   = path_combine(self.hd2_location, DEFAULT_HD2_DATA_NAME)
        self.hd2_status_location = path_combine(self.hd2_location, DEFAULT_HD2_STATUS_NAME)
        folder_create(self.hd2_location       )
        folder_create(self.hd2_data_location  )
        folder_create(self.hd2_status_location)

    def set_hd3_location(self, hd3_location):
        self.hd3_location = self.ensure_last_char_is_not_forward_slash(hd3_location)
        folder_create(self.hd3_location)


    def set_root_folder(self, root_folder=None):
        if folder_not_exists(root_folder):                                   # use temp folder if no value is provided or folder doesn't exist
            root_folder = temp_folder()

        self.root_folder = root_folder
        self.hd1_location = path_combine(root_folder, DEFAULT_HD1_NAME)      # set default values for h1, h2 and hd3
        self.hd2_location = path_combine(root_folder, DEFAULT_HD2_NAME)
        self.hd3_location = path_combine(root_folder, DEFAULT_HD3_NAME)

        self.set_hd1_location(self.hd1_location)                              # make sure folders exist
        self.set_hd2_location(self.hd2_location)
        self.set_hd3_location (self.hd3_location)
        return self

    def values(self):
        return {
            "hd1_location"       : self.hd1_location        ,
            "hd2_location"       : self.hd2_location        ,
            "hd2_data_location"  : self.hd2_data_location   ,
            "hd2_status_location": self.hd2_status_location ,
            "hd3_location"       : self.hd3_location        ,
            "root_folder"        : self.root_folder         ,
            "elastic_host"       : self.elastic_host        ,
            "elastic_port"       : self.elastic_port        ,
            "elastic_schema"     : self.elastic_schema      ,
            "kibana_host"        : self.kibana_host         ,
            "kibana_port"        : self.kibana_port         ,
            "thread_count"       : self.thread_count        ,
            "endpoints"          : self.endpoints           ,
            "request_timeout"    : self.request_timeout
        }