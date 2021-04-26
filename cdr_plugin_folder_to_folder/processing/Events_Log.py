import os
import json

import logging as logger

from osbot_utils.utils.Files import file_sha256, file_name, create_folder
from osbot_utils.utils.Json import json_save_file_pretty
from cdr_plugin_folder_to_folder.common_settings.Config import Config

from enum import Enum
from datetime import datetime 
import uuid

from cdr_plugin_folder_to_folder.utils.Log_Duration import log_duration
from cdr_plugin_folder_to_folder.utils.Logging import log_info

logger.basicConfig(level=logger.INFO)

class Events_Log:

    EVENTS_LOG_FILE_NAME = "events.json"

    def __init__(self, folder):
        self.config = Config()
        self.folder = folder
        self.data = { "events" : [] }
        self.get_from_file()
        self.unique_id = str(uuid.uuid4())

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
        create_folder(self.folder)
        json_save_file_pretty(self.data, self.get_file_path())

    def add_log(self, message, data=None):
        log_info(message=message, data=data)
        if data is str:
            data = {"str": data }
        self.get_from_file()

        json_data= {    "timestamp" : str(datetime.now()),
                        "message"   : message            ,
                        "data"      : data  or {}        ,
                        "uuid"      : self.unique_id     }

        self.data["events"].append(json_data)
        self.write_to_file()



