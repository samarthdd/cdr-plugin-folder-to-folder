import os
import json

import logging as logger

from osbot_utils.utils.Files import file_sha256, file_name, create_folder
from osbot_utils.utils.Json import json_save_file_pretty
from cdr_plugin_folder_to_folder.common_settings.Config import Config

from enum import Enum
from datetime import datetime 

logger.basicConfig(level=logger.INFO)

class Events_Log:

    EVENTS_LOG_FILE_NAME = "events.json"

    def __init__(self, folder):
        self.config = Config().load_values()
        self.folder = folder
        self.data = { "events" : [] }
        create_folder(self.folder)
        self.write_to_file()

    def get_file_path(self):
        return os.path.join(self.folder, Events_Log.EVENTS_LOG_FILE_NAME)

    def get_from_file(self):
        if not os.path.isfile(self.get_file_path()):
            return
        try:
            with open(self.get_file_path()) as json_file:
                self.data = json.load(json_file)
        except Exception as error:
            logger.error("Failed to get from file: " + self.folder)
            logger.error("Failure details: {error}")
            raise error

    def write_to_file(self):
        json_save_file_pretty(self.data, self.get_file_path())

    def add_log(self, log):
        self.get_from_file()

        json_data={}
        json_data["timestamp"] = str(datetime.now())
        json_data["log"] = log

        self.data["events"].append(json_data)
        self.write_to_file()
