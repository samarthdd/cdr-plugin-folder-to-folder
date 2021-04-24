import os
import json
import asyncio

import logging as logger
import threading

from osbot_utils.utils.Files import file_sha256, file_name, create_folder, path_combine, file_exists
from osbot_utils.utils.Json import json_save_file_pretty, json_load_file, json_save_file
from cdr_plugin_folder_to_folder.common_settings.Config import Config

from enum import Enum

from cdr_plugin_folder_to_folder.storage.Storage import Storage

logger.basicConfig(level=logger.INFO)

class FileStatus:                                     # todo move to separate file (either per enum or with all enums)
    INITIAL     = "Initial"
    IN_PROGRESS = "In Progress"
    COMPLETED   = "Completed Successfully"
    FAILED      = "Completed with errors"
    TO_PROCESS  = "To Process"
    NONE        = "None"

class Status:

    STATUS_FILE_NAME        = "status.json"
    VAR_COMPLETED           = "completed"
    VAR_CURRENT_STATUS      = "current_status"
    VAR_FAILED              = "failed"
    VAR_FILES_TO_PROCESS    = "files_to_process"
    VAR_FILES_COUNT         = "files_count"
    VAR_IN_PROGRESS         = "in_progress"

    #lock = asyncio.Lock()
    lock = threading.Lock()

    _instance = None
    def __new__(cls):                                               # singleton pattern
        if cls._instance is None:
            cls._instance = super(Status, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        #self.config = Config()
        if hasattr(self, 'folder') is False:                     # only set these values first time around
            self.storage        = Storage()
            #self._on_save      = []                             # todo: add support for firing up events when data is saved
            self._status_data   = self.default_data()
            self.load_data()

    # def load_values(self):
    #     self.folder = os.path.join(self.config.hd2_location, "status")
    #     if not self.get_from_file():
    #         self.reset()
    #

    def data(self):
        return self._status_data

    def default_data(self):
        return {    Status.VAR_CURRENT_STATUS   : FileStatus.NONE ,
                    Status.VAR_FILES_COUNT      : 0               ,
                    Status.VAR_FILES_TO_PROCESS : 0               ,
                    Status.VAR_COMPLETED        : 0               ,
                    Status.VAR_FAILED           : 0               ,
                    Status.VAR_IN_PROGRESS      : 0               }

    #def exists(self):
    #    return file_exists(self.status_file_path())

    def load_data(self):
        self._status_data = json_load_file(self.status_file_path())
        if self.data() == {}:
            self.reset()
        return self

    def reset(self):
        self._status_data = self.default_data()
        self.save()
        return self

    def save(self):
        json_save_file_pretty(self.data(), self.status_file_path())
        return self
        #json_save_file_pretty(self.data, self.get_file_path())

    def status_file_path(self):
        return path_combine(self.storage.hd2_status(), Status.STATUS_FILE_NAME)

    # def get_from_file(self):
    #     if not os.path.isfile(self.get_file_path()):
    #         return False
    #     try:
    #         with open(self.get_file_path()) as json_file:
    #             self.data = json.load(json_file)
    #     except Exception as error:
    #         logger.error("Failed to init status from file: {medadata_folder}")
    #         logger.error("Failure details: {error}")
    #         raise error
    #     return True


    # def write_to_file(self):
    #     create_folder(self.folder)
    #     json_save_file_pretty(self.data, self.get_file_path())

    def update_counters(self, updated_status):
        Status.lock.acquire()
        try:
            data = self.data()
            data[Status.VAR_CURRENT_STATUS] = updated_status

            if updated_status == FileStatus.INITIAL:
                data[Status.VAR_FILES_COUNT] += 1

            elif updated_status == FileStatus.IN_PROGRESS:
                data["in_progress"] += 1

            elif updated_status == FileStatus.COMPLETED:
                data["completed"] += 1
                if data["in_progress"] > 0:
                    data["in_progress"] -= 1
                if data["files_to_process"] > 0:
                    data["files_to_process"] -= 1

            elif updated_status == FileStatus.FAILED:
                data["failed"] += 1
                if data["in_progress"] > 0:
                    data["in_progress"] -= 1
                if data["files_to_process"] > 0:
                    data["files_to_process"] -= 1

            elif updated_status == FileStatus.TO_PROCESS:
                data["files_to_process"] += 1
            self.save()
        finally:
            Status.lock.release()
        return self

    # def update_counters(self, updated_status):
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #     loop.run_until_complete(self.update_counters_async(updated_status))

    def add_completed       (self): return self.update_counters(FileStatus.COMPLETED    )
    def add_failed          (self): return self.update_counters(FileStatus.FAILED       )
    def add_file            (self): return self.update_counters(FileStatus.INITIAL      )
    def add_in_progress     (self): return self.update_counters(FileStatus.IN_PROGRESS  )
    def add_to_be_processed (self): return self.update_counters(FileStatus.TO_PROCESS   )

    def get_completed       (self): return self.data().get(Status.VAR_COMPLETED)
    def get_current_status  (self): return self.data().get(Status.VAR_CURRENT_STATUS)
    def get_failed          (self): return self.data().get(Status.VAR_FAILED)
    def get_files_count     (self): return self.data().get(Status.VAR_FILES_COUNT)
    def get_files_to_process(self): return self.data().get(Status.VAR_FILES_TO_PROCESS)

    def get_in_progress(self):
        return self.data().get(Status.VAR_IN_PROGRESS)