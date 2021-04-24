import threading
import logging as logger

from osbot_utils.utils.Files                     import path_combine
from osbot_utils.utils.Json                      import json_save_file_pretty, json_load_file
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

    lock = threading.Lock()

    _instance = None
    def __new__(cls):                                               # singleton pattern
        if cls._instance is None:
            cls._instance = super(Status, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'folder') is False:                     # only set these values first time around
            self.storage        = Storage()
            #self._on_save      = []                             # todo: add support for firing up events when data is saved
            self._status_data   = self.default_data()
            self.load_data()

    def data(self):
        return self._status_data

    def default_data(self):
        return {    Status.VAR_CURRENT_STATUS   : FileStatus.NONE ,
                    Status.VAR_FILES_COUNT      : 0               ,
                    'files_copied'              : 0               ,
                    'files_left_to_be_copied'   : 0               ,
                    Status.VAR_FILES_TO_PROCESS : 0               ,
                    'files_left_to_process'     : 0               ,
                    Status.VAR_COMPLETED        : 0               ,
                    Status.VAR_FAILED           : 0               ,
                    Status.VAR_IN_PROGRESS      : 0               }

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

    def status_file_path(self):
        return path_combine(self.storage.hd2_status(), Status.STATUS_FILE_NAME)

    def update_counters(self, updated_status, count=0):
        Status.lock.acquire()
        try:
            data = self.data()
            data[Status.VAR_CURRENT_STATUS] = updated_status

            if updated_status == FileStatus.NONE:
                data["files_count"] += count
                data["files_left_to_be_copied"] += count
                
            elif updated_status == FileStatus.INITIAL:
                data["files_copied"] += 1
                if data["files_left_to_be_copied"] > 0:
                    data["files_left_to_be_copied"] -= 1

            elif updated_status == FileStatus.IN_PROGRESS:
                data["in_progress"] += 1

            elif updated_status == FileStatus.COMPLETED:
                data["completed"] += 1
                if data["in_progress"] > 0:
                    data["in_progress"] -= 1
                if data["files_left_to_process"] > 0:
                    data["files_left_to_process"] -= 1
            elif updated_status == FileStatus.FAILED:
                data["failed"] += 1
                if data["in_progress"] > 0:
                    data["in_progress"] -= 1
                if data["files_left_to_process"] > 0:
                    data["files_left_to_process"] -= 1

            elif updated_status == FileStatus.TO_PROCESS:
                data["files_to_process"] += 1
                data["files_left_to_process"] += 1

            if updated_status == FileStatus.INITIAL:
                data[Status.VAR_FILES_COUNT] += 1
        finally:
            Status.lock.release()
            self.save()

        return self

    def add_completed       (self       ): return self.update_counters(FileStatus.COMPLETED          )
    def add_failed          (self       ): return self.update_counters(FileStatus.FAILED             )
    def add_file            (self       ): return self.update_counters(FileStatus.INITIAL            )
    def add_files_count     (self, count): return self.update_counters(FileStatus.NONE        , count)
    def add_in_progress     (self       ): return self.update_counters(FileStatus.IN_PROGRESS        )
    def add_to_be_processed (self       ): return self.update_counters(FileStatus.TO_PROCESS         )

    def get_completed       (self): return self.data().get(Status.VAR_COMPLETED)
    def get_current_status  (self): return self.data().get(Status.VAR_CURRENT_STATUS)
    def get_failed          (self): return self.data().get(Status.VAR_FAILED)
    def get_files_count     (self): return self.data().get(Status.VAR_FILES_COUNT)
    def get_files_to_process(self): return self.data().get(Status.VAR_FILES_TO_PROCESS)
    def get_in_progress     (self): return self.data().get(Status.VAR_IN_PROGRESS)
