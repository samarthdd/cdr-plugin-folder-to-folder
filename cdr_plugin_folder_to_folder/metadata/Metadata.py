import os
import json

from osbot_utils.utils.Files import file_name, folder_exists, file_sha256, file_exists, folder_create, path_combine, \
    folder_delete_all, file_copy
from osbot_utils.utils.Json import json_save_file_pretty
from osbot_utils.utils.Misc import datetime_now

from cdr_plugin_folder_to_folder.metadata.Metadata_Utils import Metadata_Utils
from cdr_plugin_folder_to_folder.pre_processing.Status import Status, FileStatus
from cdr_plugin_folder_to_folder.storage.Storage import Storage

DEFAULT_METADATA_FILENAME = "metadata.json"
DEFAULT_SOURCE_FILENAME   = "source"

class Metadata:

    def __init__(self, file_hash=None):
        self.storage        = Storage()
        self.process_status = Status()
        self.metadata_utils = Metadata_Utils()
        self.path_hd1       = self.storage.hd1()
        self.data           = self.default_data()
        self.file_hash      = file_hash

    def get_from_file(self):
        with open(self.metadata_file_path()) as json_file:
            self.data = json.load(json_file)

    def add_file(self, file_path):
        if file_exists(file_path):
            self.set_file_hash(self.metadata_utils.file_hash(file_path))
            if self.exists():
                self.get_from_file()
            else:
                self.create(file_path)
            self.add_file_path(file_path)
            self.save()
            return self.file_hash

    def add_file_path(self, file_path:str):
        if self.file_hash:
            file_paths = self.data.get('original_file_paths')
            if 0 == len(file_paths):
                self.process_status.add_to_be_processed()
            if file_path.startswith(self.path_hd1):                         # check if path starts with hd1
                file_path = os.path.relpath(file_path, self.path_hd1)
            if file_path not in file_paths:
                file_paths.append(file_path)
            return file_paths

    def create(self, file_path):
        if self.file_hash:
            folder_create(self.metadata_folder_path())
            file_copy    (file_path, self.source_file_path())
            self.set_file_name(file_name(file_path))

    def default_data(self):
        return {   'file_name'              : None                      ,
                   'xml_report_status'      : None                      ,
                   'last_update_time'       : None                      ,
                   'rebuild_server'         : None                      ,
                   'server_version'         : None                      ,
                   'error'                  : None                      ,
                   'original_file_paths'    : []                        ,
                   'original_hash'          : None                      ,
                   'original_file_extension': None                      ,
                   'original_file_size'     : None                      ,
                   'rebuild_file_path'      : None                      ,
                   'rebuild_hash'           : None                      ,
                   'rebuild_status'         : FileStatus.INITIAL.value  ,
                   'rebuild_file_extension' : None                      ,
                   'rebuild_file_size'      : None                      ,
                   'rebuild_file_duration'  : None                      ,
                   'f2f_plugin_version'     : None                      ,
                   'f2f_plugin_git_commit'  : None
                 }

    def delete(self):
        if self.exists():
            folder_delete_all(self.metadata_folder_path())
            return self.exists() is False
        return False

    def exists(self):
        return folder_exists(self.metadata_folder_path())

    # def load(self):
    #     #self.file_hash = file_hash
    #     pass

    def metadata_file_path(self):
        if self.file_hash:
            return path_combine(self.metadata_folder_path(), DEFAULT_METADATA_FILENAME)

    def metadata_folder_path(self):
        if self.file_hash:
            return self.storage.hd2_data(self.file_hash)

    def save(self):
        if self.exists():
            json_save_file_pretty(python_object=self.data, path=self.metadata_file_path())

    def update_field(self, field, updated_value):
        self.data[field] = updated_value
        self.data['last_update_time'] = datetime_now()
        self.save()

    def set_file_hash(self, file_hash):
        self.file_hash = file_hash
        self.data['original_hash'] = file_hash
        self.data['last_update_time'] = datetime_now()
        if not self.exists():
            self.save()

    def set_file_name(self, file_name):
        self.update_field('file_name', file_name)

    def source_file_path(self):
        if self.file_hash:
            return path_combine(self.metadata_folder_path(), DEFAULT_SOURCE_FILENAME)

    def get_original_hash(self):
        return self.data.get('original_hash')

    def get_file_name(self):
        return self.data.get('file_name')

    def get_rebuild_status(self):
        return self.data.get('rebuild_status')

    def get_original_file_paths(self):
        return self.data.get('original_file_paths')

    def get_last_update_time(self):
        return self.data.get('last_update_time')

