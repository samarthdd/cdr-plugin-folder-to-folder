import os
import json

import logging as logger
import re

from osbot_utils.utils.Files import create_folder
from osbot_utils.utils.Json import json_save_file_pretty, json_load_file
from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.pre_processing.Status import FileStatus

from enum import Enum

from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.utils.Logging import log_error
from cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Utils.Misc import is_regex_full_match

logger.basicConfig(level=logger.INFO)

class Hash_Json:

    HASH_FILE_NAME = "hash.json"
    REGEX_HASH     = '[A-Fa-f0-9]{64}$'

    def __init__(self):
        self.config  = Config()
        self.storage = Storage()
        self.folder  = os.path.join(self.config.hd2_location, "status")
        self.data    = {}
        self.id      = 0
        self.get_from_file()

    def add_file(self, file_hash, file_name):
        if self.is_hash(file_hash) and file_name:
            json_value  = {"file_name"  : file_name,
                           "file_status": FileStatus.INITIAL}

            json_data   = {file_hash: json_value}

            self.data.update(json_data)
            self.write_to_file()
            return True
        log_error(message='in Hash_Json.add_file bad data provided', data = {'file_hash': file_hash, 'file_name': file_name})
        return False

    def get_file_path(self):
        return os.path.join(self.folder, Hash_Json.HASH_FILE_NAME)

    def get_from_file(self):
        self.data = json_load_file(self.get_file_path())
        return self.data

    def get_json_list(self):
        return self.data

    def is_hash(self, value):
        return is_regex_full_match(Hash_Json.REGEX_HASH, value)

    def reset(self):
        self.data = {}
        self.write_to_file()
        return self

    def write_to_file(self):
        create_folder(self.folder)
        json_save_file_pretty(self.data, self.get_file_path())

    def update_status(self, index, updated_status):
        self.data[index]["file_status"] = updated_status
        self.write_to_file()





