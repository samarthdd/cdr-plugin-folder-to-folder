import os
import json

import logging as logger

from osbot_utils.utils.Files import file_sha256, file_name, create_folder
from osbot_utils.utils.Json import json_save_file_pretty
from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.pre_processing.Status import FileStatus

from enum import Enum

logger.basicConfig(level=logger.INFO)

class Hash_Json:

    HASH_FILE_NAME = "hash.json"

    def __init__(self):
        self.config = Config().load_values()
        self.folder = os.path.join(self.config.hd2_location, "status")
        self.data = { "file_list" : []  }
        self.id = 0
        self.get_from_file()

    def get_file_path(self):
        return os.path.join(self.folder, Hash_Json.HASH_FILE_NAME)

    def get_from_file(self):
        if not os.path.isfile(self.get_file_path()):
            return
        try:
            with open(self.get_file_path()) as json_file:
                self.data = json.load(json_file)
        except Exception as error:
            logger.error("Failed to init status from file: {medadata_folder}")
            logger.error("Failure details: {error}")
            raise error
        return self.data

    def write_to_file(self):
        create_folder(self.folder)
        json_save_file_pretty(self.data, self.get_file_path())

    def add_file(self, hash, file_name):

        json_data={}

        json_data["id"] = self.id
        self.id=self.id+1

        json_data["hash"] = hash
        json_data["file_name"] = file_name
        json_data["file_status"] = FileStatus.INITIAL.value
        self.data["file_list"].append(json_data)

        self.write_to_file()

    def get_file_list(self):
        return self.data["file_list"]

    def update_status(self, index, updated_status):
        self.data["file_list"][index]["file_status"] = updated_status

