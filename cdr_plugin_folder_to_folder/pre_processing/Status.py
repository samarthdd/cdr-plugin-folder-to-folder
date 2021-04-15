import os
import json
import asyncio

import logging as logger

from osbot_utils.utils.Files import file_sha256, file_name
from osbot_utils.utils.Json import json_save_file_pretty
from cdr_plugin_folder_to_folder.common_settings.Config import Config

from enum import Enum

logger.basicConfig(level=logger.INFO)

class FileStatus(Enum):
    INITIAL = "Initial"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed Successfully"
    FAILED = "Completed with errors" 

class Status:

    STATUS_FILE_NAME = "status.json"
    lock = asyncio.Lock()

    def __init__(self):
        self.config = Config().load_values()
        self.folder = os.path.join(self.config.hd2_location, "status")
        self.data = {   "files_count"          : 0     ,
                        "files_to_process"     : 0     ,
                        "completed"            : 0     ,
                        "failed"               : 0     ,
                        "in_progress"          : 0
                    }
        self.id = 0

    def get_file_path(self):
        return os.path.join(self.folder, Status.STATUS_FILE_NAME)

    def get_from_file(self):
        try:
            with open(self.get_file_path()) as json_file:
                self.data = json.load(json_file)
        except Exception as error:
            logger.error("Failed to init status from file: {medadata_folder}")
            logger.error("Failure details: {error}")
            raise error
        return self.data

    def write_to_file(self):
        json_save_file_pretty(self.data, self.get_file_path())

    def add_file(self):
        self.data["files_count"] += 1

    async def update_counters_async(self, index, updated_status):
        await Status.lock.acquire()
        try:
            if updated_status == FileStatus.IN_PROGRESS.value:
                self.data["in_progress"] += 1
            elif updated_status == FileStatus.COMPLETED.value:
                self.data["completed"] += 1
            elif updated_status == FileStatus.FAILED.value:
                self.data["failed"] += 1
        finally:
            Status.lock.release()

    def update_counters(self, index, updated_status):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.update_counters_async(index, updated_status))
