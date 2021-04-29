import os
import logging as logger
from datetime import datetime
from osbot_utils.utils.Files import folder_create, folder_delete_all, folder_copy

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.utils.Log_Duration import log_duration

from cdr_plugin_folder_to_folder.pre_processing.Status import Status, FileStatus
from cdr_plugin_folder_to_folder.pre_processing.Hash_Json import Hash_Json

from cdr_plugin_folder_to_folder.processing.Analysis_Json import Analysis_Json

logger.basicConfig(level=logger.INFO)

class Pre_Processor:

    def __init__(self):
        self.config         = Config()
        self.meta_service   = Metadata_Service()
        self.status         = Status()
        self.storage        = Storage()
        self.file_name      = None                              # set in process() method
        self.current_path   = None
        self.base_folder    = None
        self.dst_folder     = None
        self.dst_file_name  = None

        self.hash_json = Hash_Json()
        self.status = Status()
        self.status.reset()

        #self.analysis_json = Analysis_Json()

    @log_duration
    def clear_data_and_status_folders(self):
        data_target     = self.storage.hd2_data()       # todo: refactor this clean up to the storage class
        status_target   = self.storage.hd2_status()
        folder_delete_all(data_target)
        folder_delete_all(status_target)
        folder_create(data_target)
        folder_create(status_target)
        self.status.reset()

    def file_hash(self, file_path):
        return self.meta_service.file_hash(file_path)

    def prepare_folder(self, folder_to_process):
        if folder_to_process.startswith(self.storage.hd1()):
            return folder_to_process

        dirname = os.path.join(self.storage.hd1(), os.path.basename(folder_to_process))
        if os.path.isdir(dirname):
            folder_delete_all(dirname)
        try:
            folder_copy(folder_to_process, dirname)
        finally:
            return dirname

    def process_folder(self, folder_to_process):
        if not os.path.isdir(folder_to_process):
            # todo: add an event log
           return False

        folder_to_process = self.prepare_folder(folder_to_process)

        files_count = 0

        for folderName, subfolders, filenames in os.walk(folder_to_process):
            for filename in filenames:
                file_path =  os.path.join(folderName, filename)
                if os.path.isfile(file_path):
                    files_count += 1

        self.status.add_files_count(files_count)

        for folderName, subfolders, filenames in os.walk(folder_to_process):
            for filename in filenames:
                file_path =  os.path.join(folderName, filename)
                if os.path.isfile(file_path):
                    self.process(file_path)

        self.hash_json.save()

        return True

    @log_duration
    def process_files(self):
        self.status.set_phase_1()
        self.process_folder(self.storage.hd1())
        self.hash_json.reset()
        self.hash_json.save()
        self.status.set_phase_2()

    @log_duration
    def process(self, file_path):
        tik  = datetime.now()

        metadata = self.meta_service.create_metadata(file_path=file_path)
        file_name      = metadata.get_file_name()
        original_hash  = metadata.get_original_hash()
        status         = metadata.get_rebuild_status()
        self.update_status(file_name, original_hash, status)

        tok   = datetime.now()
        delta = tok - tik

        hash_folder_path = os.path.join(self.storage.hd2_data(), original_hash)
        self.meta_service.set_hd1_to_hd2_copy_time(hash_folder_path, delta.total_seconds())

    def update_status(self, file_name, original_hash, status):
        if status == FileStatus.INITIAL:
            self.status.add_file()
