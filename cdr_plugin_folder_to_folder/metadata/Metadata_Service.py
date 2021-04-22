import hashlib
import json
import os

import logging as logger

from osbot_utils.utils.Files import file_sha256, file_name
from osbot_utils.utils.Json import json_save_file_pretty
from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.metadata.Metadata import Metadata
from cdr_plugin_folder_to_folder.pre_processing.Status import FileStatus

from enum import Enum

from cdr_plugin_folder_to_folder.metadata.Metadata_Elastic import Metadata_Elastic

logger.basicConfig(level=logger.INFO)

class Metadata_Service:

    METADATA_FILE_NAME = "metadata.json"

    def __init__(self):
        self.file_path        = None
        self.metadata_folder  = None
        self.metadata         = None
        self.config           = Config()
        self.metadata_elastic = Metadata_Elastic().setup()

    def create_metadata(self, file_path):
        self.metadata = Metadata()
        self.metadata.add_file(file_path)
        self.metadata_elastic.add_metadata(self.metadata.data)                            # save metadata to elastic
        return self.metadata

    def get_from_file(self, metadata_folder):
        self.metadata = Metadata(os.path.basename(metadata_folder))
        self.metadata.get_from_file()
        self.metadata_folder=metadata_folder
        return self.metadata

    def get_metadata_file_path(self):
        return os.path.join(self.metadata_folder, Metadata_Service.METADATA_FILE_NAME)

    def file_hash(self, file_path):
        return file_sha256(file_path)

    def get_original_file_paths(self, metadata_folder):
        self.get_from_file(metadata_folder)
        return self.metadata.get_original_file_paths()

    def get_status(self, metadata_folder):
        self.get_from_file(metadata_folder)
        return self.metadata.get_rebuild_status()

    def is_initial_status(self, metadata_folder):
        return (self.get_status(metadata_folder) == FileStatus.INITIAL.value)

    def set_status_inprogress(self, metadata_folder):
        self.set_status(metadata_folder, FileStatus.IN_PROGRESS.value)

    def set_metadata_field(self, metadata_folder, field_name, value):
        self.get_from_file(metadata_folder)
        self.metadata.update_field(field_name, value)
        self.metadata_elastic.add_metadata(self.metadata.data) # save metadata to elastic

    def set_status(self, metadata_folder, rebuild_status):
        self.set_metadata_field(metadata_folder, 'rebuild_status', rebuild_status)

    def set_error(self, metadata_folder, error_details):
        self.set_metadata_field(metadata_folder, 'error', error_details)
