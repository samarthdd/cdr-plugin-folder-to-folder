import os
import json
import ntpath

import logging as logger

from osbot_utils.utils.Files import temp_folder, path_combine, folder_create, folder_delete_all
from osbot_utils.utils.Misc import timestamp_utc_now

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.pre_processing.utils.file_service import File_Service
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.utils.Elastic import Elastic
from cdr_plugin_folder_to_folder.utils.Log_Duration import Log_Duration, log_duration
from cdr_plugin_folder_to_folder.utils.Logging import Logging, log_info, log_debug

logger.basicConfig(level=logger.INFO)

class Pre_Processor:

    def __init__(self):

        self.filename       =  None
        self.hd1_path       =  None
        self.original_hash  =  None
        self.config         = Config().load_values()
        self.temp_folder    = temp_folder()                                     # todo: this should be deleted after file processing
        self.hd1_location   = self.config.hd1_location
        self.data_target    =  path_combine(self.config.hd2_location , "data")
        self.status_target  =  path_combine(self.config.hd2_location , "status")

        self.file_service   =  File_Service()
        self.meta_service   =  Metadata_Service()

        self.hash_json      =  []
        self.id             =  0

        self.file_name      = None                              # set in process() method
        self.current_path   = None
        self.base_folder    = None
        self.dst_folder     = None
        self.dst_file_name  = None

        folder_create(self.data_target)                             # todo: refactor this from this __init__
        folder_create(self.status_target)

        self.logging = Logging()


    @log_duration
    def clear_data_and_status_folders(self):
        folder_delete_all(self.data_target)
        folder_delete_all(self.status_target)
        folder_create(self.data_target)
        folder_create(self.status_target)

    @log_duration
    def process_files(self):
        try:
            for folderName, subfolders, filenames in os.walk(self.hd1_location):
                for filename in filenames:
                    self.hd1_path =  os.path.join(folderName, filename)
                    if os.path.isfile(self.hd1_path):
                        self.process(self.hd1_path)
        except Exception as error:
            logger.error(f"PreProcessor: process_files : {error}")
            raise error

    @log_duration
    def process(self, file_path):
        try:
            self.file_name = ntpath.basename(file_path)
            self.hd1_path  = file_path

            # Copy File to temp path
            self.current_path = os.path.join(self.temp_folder, self.file_name)
            self.file_service.copy_file(self.hd1_path,self.current_path)

            # Get metadata
            metadata_content=self.meta_service.get_metadata(file_path=self.current_path,hd1_path=self.hd1_path)


            # Get SHA 256 hash
            self.original_hash = metadata_content["original_hash"]

            # Create basefolder
            self.base_folder = os.path.join(self.temp_folder, self.original_hash)
            self.file_service.create_folder(folder_name=self.base_folder)

            # target folder
            self.dst_folder = os.path.join(self.data_target, self.original_hash)

            # Check hash folder exists in HD2
            if not os.path.exists(self.dst_folder):

                self.dst_file_name = "source"

                # Store metadata
                metadata_content["hd2_path"] = os.path.join(self.dst_folder, self.dst_file_name)
                self.meta_service.write_metadata_to_file(metadata_content, self.base_folder)

                # Rename and Move original file to hash folder
                self.file_service.move_file(self.current_path,
                                            os.path.join(self.base_folder, self.dst_file_name))

                # Store hash folder to HD2
                self.file_service.copy_folder(self.base_folder, self.dst_folder)
                self.update_status()
            else:
                # Update HD2 metadata with source paths
                self.update_hd2_metadata()
                # Remove temp file
                os.remove(self.current_path)

            # Delete temp hash folder
            self.file_service.delete_folder(self.base_folder)

        except Exception as error:
            logger.error(f"PreProcessor: process : {error}")
            raise error

    def update_hd2_metadata(self):
        try:
            # Update HD2 metadata with source paths
            src  = os.path.join(self.dst_folder, Metadata_Service.METADATA_FILE_NAME)
            dst  = os.path.join(self.base_folder, Metadata_Service.METADATA_FILE_NAME)

            self.file_service.copy_file( src, dst)

            metadata_content   = self.meta_service.get_from_file(self.base_folder)
            if metadata_content["original_file_paths"] != self.hd1_path:
                metadata_content["original_file_paths"] = metadata_content["original_file_paths"]+ "," + self.hd1_path
                self.meta_service.write_metadata_to_file(metadata_content,self.dst_folder)
                self.file_service.copy_file(dst,src)
        except Exception as error:
            raise error

    def update_status(self):
        try:
            self.id=self.id+1
            json_data={}

            json_data["id"]=self.id
            json_data["file_name"]=self.file_name
            json_data["original_hash"]=self.original_hash

            self.hash_json.append(json_data)
            hash_file_name="hash.json"

            self.file_service.wrtie_json_file(self.status_target,hash_file_name,self.hash_json)
        except Exception as error:
            raise error