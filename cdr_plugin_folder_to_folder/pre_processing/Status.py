import os
import json
import asyncio

import logging as logger

from osbot_utils.utils.Files import file_sha256, file_name, create_folder
from osbot_utils.utils.Json import json_save_file_pretty
from cdr_plugin_folder_to_folder.common_settings.Config import Config

from enum import Enum

logger.basicConfig(level=logger.INFO)

class FileStatus(Enum):
    INITIAL     = "Initial"
    IN_PROGRESS = "In Progress"
    COMPLETED   = "Completed Successfully"
    FAILED      = "Completed with errors"
    TO_PROCESS  = "To Process"

class Status:

    STATUS_FILE_NAME = "status.json"
    lock = asyncio.Lock()

    _instance = None
    def __new__(cls):                                               # singleton pattern
        if cls._instance is None:
            cls._instance = super(Status, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'folder') is False:                     # only set these values first time around
            self.config = Config()
            self.folder = os.path.join(self.config.hd2_location, "status")
            if not self.get_from_file():
                self.reset()

    def reset(self):
        self.data = {   "files_count"          : 0     ,
                        "files_to_process"     : 0     ,
                        "completed"            : 0     ,
                        "failed"               : 0     ,
                        "in_progress"          : 0
                    }

    def get_file_path(self):
        return os.path.join(self.folder, Status.STATUS_FILE_NAME)

    def get_from_file(self):
        if not os.path.isfile(self.get_file_path()):
            return False
        try:
            with open(self.get_file_path()) as json_file:
                self.data = json.load(json_file)
        except Exception as error:
            logger.error("Failed to init status from file: {medadata_folder}")
            logger.error("Failure details: {error}")
            raise error
        return True

    def write_to_file(self):
        create_folder(self.folder)
        json_save_file_pretty(self.data, self.get_file_path())

    async def update_counters_async(self, updated_status):
        await Status.lock.acquire()
        try:
            if updated_status == FileStatus.INITIAL:
                self.data["files_count"] += 1
            elif updated_status == FileStatus.IN_PROGRESS:
                self.data["in_progress"] += 1
            elif updated_status == FileStatus.COMPLETED:
                self.data["completed"] += 1
                if self.data["in_progress"] > 0:
                    self.data["in_progress"] -= 1
                if self.data["files_to_process"] > 0:
                    self.data["files_to_process"] -= 1
            elif updated_status == FileStatus.FAILED:
                self.data["failed"] += 1
                if self.data["in_progress"] > 0:
                    self.data["in_progress"] -= 1
                if self.data["files_to_process"] > 0:
                    self.data["files_to_process"] -= 1
            elif updated_status == FileStatus.TO_PROCESS:
                self.data["files_to_process"] += 1
        finally:
            Status.lock.release()

    def update_counters(self, updated_status):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.update_counters_async(updated_status))

    def add_file(self):
        self.update_counters(FileStatus.INITIAL)

    def add_completed(self):
        self.update_counters(FileStatus.COMPLETED)

    def add_failed(self):
        self.update_counters(FileStatus.FAILED)

    def add_in_progress(self):
        self.update_counters(FileStatus.IN_PROGRESS)

    def add_to_be_processed(self):
        self.update_counters(FileStatus.TO_PROCESS)