import os
import logging as logger

from osbot_utils.utils.Files import folder_create, folder_delete_all

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.utils.Elastic import Elastic
from cdr_plugin_folder_to_folder.utils.Log_Duration import Log_Duration, log_duration
from cdr_plugin_folder_to_folder.utils.Logging import Logging, log_info, log_debug
from osbot_utils.utils.Json import json_save_file_pretty
from cdr_plugin_folder_to_folder.pre_processing.Status import Status, FileStatus

logger.basicConfig(level=logger.INFO)

class Pre_Processor:

    def __init__(self):
        self.config         = Config()
        self.meta_service   = Metadata_Service()
        self.status         = Status()
        self.storage        = Storage()
        #self.filename       =  None
        #self.hd1_path       =  None
        #self.original_hash  =  None
        #self.temp_folder    =  temp_folder()                                     # todo: this should be deleted after file processing
        #self.hd1_location   =  self.config.hd1_location
        #self.data_target    =  path_combine(self.config.hd2_location , "data")
        #self.status_target  =  path_combine(self.config.hd2_location , "status")

        #self.file_service   =  File_Service()


        #self.hash_json      =  []

        #self.file_name      = None                              # set in process() method
        #self.current_path   = None
        #self.base_folder    = None
        #self.dst_folder     = None
        #self.dst_file_name  = None



        #folder_create(self.data_target)                             # todo: refactor this from this __init__
        #folder_create(self.status_target)

        #self.logging = Logging()


    @log_duration
    def clear_data_and_status_folders(self):
        data_target     = self.storage.hd2_data()       # todo: refactor this clean up to the storage class
        status_target   = self.storage.hd2_status()
        folder_delete_all(data_target)
        folder_delete_all(status_target)
        folder_create(data_target)
        folder_create(status_target)

    def file_hash(self, file_path):
        return self.meta_service.file_hash(file_path)

    # def file_hash_metadata(self, file_hash):
    #     return self.meta_service.file_hash_metadata()
    #     pass

    def process_files(self):
        try:
            hd1_location = self.storage.hd1()
            for folderName, subfolders, filenames in os.walk(hd1_location):     # refactor this to be provided from the storage class
                for filename in filenames:
                    self.hd1_path =  os.path.join(folderName, filename)
                    if os.path.isfile(self.hd1_path):
                        self.process(self.hd1_path)
        except Exception as error:
            logger.error(f"PreProcessor: process_files : {error}")
            raise error

    def process(self, file_path):
        try:

            metadata = self.meta_service.create_metadata(file_path=file_path)

            #self.hd1_path       = file_path
            file_name      = metadata.file_name()
            original_hash  = metadata.original_hash()
            status         = metadata.status()
            self.update_status(file_name, original_hash, status)
            # self.file_name = ntpath.basename(file_path)
            # self.hd1_path  = file_path
            #
            # # Copy File to temp path
            # self.current_path = os.path.join(self.temp_folder, self.file_name)
            # self.file_service.copy_file(self.hd1_path,self.current_path)
            #
            # # Get metadata
            # metadata = self.meta_service.create_metadata(file_path=self.current_path)
            # metadata_content = metadata.data
            #
            #
            # # Get SHA 256 hash
            # self.original_hash = metadata_content["original_hash"]
            #
            # # Create basefolder
            # self.base_folder = os.path.join(self.temp_folder, self.original_hash)
            # self.file_service.create_folder(folder_name=self.base_folder)
            #
            # # target folder
            # self.dst_folder = os.path.join(self.data_target, self.original_hash)
            #
            # # Check hash folder exists in HD2
            # if not os.path.exists(self.dst_folder):
            #
            #     self.dst_file_name = "source"
            #
            #     # Store metadata
            #     metadata_content["hd2_path"] = os.path.join(self.dst_folder, self.dst_file_name)
            #     self.meta_service.write_metadata_to_file(metadata_content, self.base_folder)
            #
            #     # Rename and Move original file to hash folder
            #     self.file_service.move_file(self.current_path,
            #                                 os.path.join(self.base_folder, self.dst_file_name))
            #
            #     # Store hash folder to HD2
            #     self.file_service.copy_folder(self.base_folder, self.dst_folder)
            #     self.update_status()
            # else:
            #     # Update HD2 metadata with source paths
            #     metadata.add_file(file_path)
            #
            #     # Remove temp file
            #     os.remove(self.current_path)
            #
            # # Delete temp hash folder
            # self.file_service.delete_folder(self.base_folder)

        except Exception as error:
            logger.error(f"PreProcessor: process : {error}")
            raise error

    # def update_hd2_metadata(self):
    #     try:
    #         # Update HD2 metadata with source paths
    #         src  = os.path.join(self.dst_folder, Metadata_Service.METADATA_FILE_NAME)
    #         dst  = os.path.join(self.base_folder, Metadata_Service.METADATA_FILE_NAME)
    #
    #         self.file_service.copy_file( src, dst)
    #
    #         metadata_content   = self.meta_service.get_from_file(self.base_folder)
    #         if metadata_content["ofile_paths"] != self.hd1_path:
    #             metadata_content["file_paths"] = metadata_content["file_paths"]+ "," + self.hd1_path
    #             self.meta_service.write_metadata_to_file(metadata_content,self.dst_folder)
    #             self.file_service.copy_file(dst,src)
    #     except Exception as error:
    #         raise error

    def update_status(self, file_name, original_hash, status):
        try:
            if status == FileStatus.INITIAL.value:
                self.status.add_file(original_hash, file_name)
                self.status.write_to_file()
        except Exception as error:
            raise error