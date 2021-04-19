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
        metadata = Metadata()
        metadata.add_file(file_path)
        return metadata

    # def set_metadata(self, metadata):
    #     self.metadata = metadata

    def get_from_file(self, metadata_folder):
        self.metadata_folder=metadata_folder

        with open(self.get_metadata_file_path()) as json_file:
            self.metadata = json.load(json_file)
        #except Exception as error:
        #    logger.error("Failed to init metadata from file: {medadata_folder}")
        #    logger.error("Failure details: {error}")
        #    raise error
        return self.metadata

    def get_metadata_file_path(self):
        return os.path.join(self.metadata_folder, Metadata_Service.METADATA_FILE_NAME)

    def file_hash(self, file_path):
        return file_sha256(file_path)

    def get_original_file_path(self, metadata_folder):
        self.get_from_file(metadata_folder)
        return self.metadata["original_file_paths"]

    def get_processed_file_path(self, metadata_folder):
        self.get_from_file(metadata_folder)
        path = self.metadata["original_file_paths"][0]
        if path.startswith(self.config.hd1_location):
            path = path.replace(self.config.hd1_location, self.config.hd3_location)
        else:
            path = os.path.join(self.config.hd3_location, file_name(path))
        return path

    def get_status(self, metadata_folder):
        self.get_from_file(metadata_folder)
        return self.metadata["rebuild_status"]

    def is_initial_status(self, metadata_folder):
        return (self.get_status(metadata_folder) == FileStatus.INITIAL.value)

    def set_status(self, metadata_folder, status):
        self.get_from_file(metadata_folder)
        self.metadata["rebuild_status"] = status
        self.write_metadata_to_file(self.metadata, metadata_folder)

    def set_status_inprogress(self, metadata_folder):
        self.set_status(metadata_folder, FileStatus.IN_PROGRESS.value)

    def set_error(self, metadata_folder, error_details):
        self.get_from_file(metadata_folder)
        self.metadata["error"] = error_details
        self.write_metadata_to_file(self.metadata, metadata_folder)

    def write_metadata_to_file(self, metadata, metadata_folder):
        self.metadata = metadata
        self.metadata_folder = metadata_folder
        json_save_file_pretty(self.metadata, self.get_metadata_file_path())     # save metadata to file storage
        self.metadata_elastic.add_metadata(metadata)                            # save metadata to elastic