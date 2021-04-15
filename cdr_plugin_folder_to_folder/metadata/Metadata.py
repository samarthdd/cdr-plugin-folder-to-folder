import os

from osbot_utils.utils.Files import file_name, folder_exists, file_sha256, file_exists, folder_create, path_combine, \
    folder_delete_all, file_copy
from osbot_utils.utils.Json import json_save_file_pretty

from cdr_plugin_folder_to_folder.metadata.Metadata_Utils import Metadata_Utils
from cdr_plugin_folder_to_folder.pre_processing.Status import FileStatus
from cdr_plugin_folder_to_folder.storage.Storage import Storage

DEFAULT_METADATA_FILENAME = "metadata.json"
DEFAULT_SOURCE_FILENAME   = "source"

class Metadata:

    def __init__(self, file_hash=None):
        self.storage        = Storage()
        self.metadata_utils = Metadata_Utils()
        self.path_hd1       = self.storage.hd1()
        self.data           = self.default_data()
        self.file_hash      = file_hash

    def add_file(self, file_path):
        if file_exists(file_path):
            self.set_file_hash(self.metadata_utils.file_hash(file_path))
            if self.exists() is False:
                self.create(file_path)
            self.add_file_path(file_path)
            self.save()
            return self.file_hash

    def add_file_path(self, file_path:str):
        if self.file_hash:
            file_paths = self.data.get('original_file_paths')
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
        return {   "file_name"          : None                      ,
                   "original_file_paths": []                        ,
                   "original_hash"      : None                      ,
                   'rebuild_hash'       : None                      ,
                   "rebuild_status"     : FileStatus.INITIAL.value  ,
                   "xml_report_status"  : None                      ,
                   "target_path"        : None                      ,
                   "error"              : None
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

    def set_file_hash(self, file_hash):
        self.file_hash = file_hash
        self.data['original_hash'] = file_hash

    def set_file_name(self, file_name):
        self.data['file_name'] = file_name

    def source_file_path(self):
        if self.file_hash:
            return path_combine(self.metadata_folder_path(), DEFAULT_SOURCE_FILENAME)
    # data wrappers

    def original_hash(self):
        return self.data.get('original_hash')

    def file_name(self):
        return self.data.get('file_name')

    def status(self):
        return self.data.get('rebuild_status')

