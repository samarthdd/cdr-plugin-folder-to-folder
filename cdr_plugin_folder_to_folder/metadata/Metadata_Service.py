import hashlib
import json
import os

import logging as logger

from osbot_utils.utils.Files import file_sha256, file_name
from osbot_utils.utils.Json import json_save_file_pretty
from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.pre_processing.Status import FileStatus

from enum import Enum

logger.basicConfig(level=logger.INFO)

class Metadata_Service:

    METADATA_FILE_NAME = "metadata.json"

    def __init__(self):
        self.file_path = None
        self.medadata_folder = None
        self.metadata = {}
        self.config = Config().load_values()

    def get_metadata(self, file_path, hd1_path):
        # Create metadata json
        self.file_path=file_path
        self.metadata = {"file_name"          : file_name(self.file_path)     ,
                    "original_file_paths": hd1_path                      ,  # todo: DC: check why we need this (since I think this is part of the file_path variable)
                    "original_hash"      : self.get_hash(self.file_path) ,
                    "evidence_file_paths": None                          ,
                    "rebuild_status"     : FileStatus.INITIAL.value      ,
                    "xml_report_status"  : None                          ,
                    "target_path"        : None                          ,
                    "error"              : None
                     }

        return self.metadata

    def set_metadata(self, metadata):
        self.metadata = metadata

    def get_metadata_file_path(self):
        return os.path.join(self.medadata_folder, Metadata_Service.METADATA_FILE_NAME)

    def get_from_file(self, medadata_folder):
        self.medadata_folder=medadata_folder
        try:
            with open(self.get_metadata_file_path()) as json_file:
                self.metadata = json.load(json_file)
        except Exception as error:
            logger.error("Failed to init metadata from file: {medadata_folder}")
            logger.error("Failure details: {error}")
            raise error
        return self.metadata

    def write_metadata_to_file(self, metadata, medadata_folder):
        self.metadata = metadata
        self.medadata_folder = medadata_folder
        json_save_file_pretty(self.metadata, self.get_metadata_file_path())

    def get_hash(self,file_path):
        return file_sha256(file_path)

    def get_original_file_path(self, medadata_folder):
        self.get_from_file(medadata_folder)
        return self.metadata["original_file_paths"]

    def get_processed_file_path(self, medadata_folder):
        self.get_from_file(medadata_folder)
        path = self.metadata["original_file_paths"]
        path = path.replace(self.config.hd1_location, self.config.hd3_location)
        print(path)
        return path

    def get_status(self, medadata_folder):
        self.get_from_file(medadata_folder)
        return self.metadata["rebuild_status"]

    def is_initial_status(self, medadata_folder):
        return (self.get_status(medadata_folder) == FileStatus.INITIAL.value)

    def set_status(self, medadata_folder, status):
        self.get_from_file(medadata_folder)
        self.metadata["rebuild_status"] = status
        self.write_metadata_to_file(self.metadata, medadata_folder)

    def set_status_inprogress(self, medadata_folder):
        self.set_status(medadata_folder, FileStatus.IN_PROGRESS.value)

    def set_error(self, medadata_folder, error_details):
        self.get_from_file(medadata_folder)
        self.metadata["error"] = error_details
        self.write_metadata_to_file(self.metadata, medadata_folder)
