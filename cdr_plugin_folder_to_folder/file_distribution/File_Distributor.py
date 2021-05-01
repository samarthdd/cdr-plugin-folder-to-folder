import os
from cdr_plugin_folder_to_folder.common_settings.Config import Config
import ntpath
import logging as logger
from os import environ
from osbot_utils.utils.Files import folder_exists, zip_files,temp_folder, file_exists, folder_temp,file_delete, folder_delete_all, temp_file, \
    file_copy,file_contents,folder_copy,create_folder
from cdr_plugin_folder_to_folder.storage.Storage import Storage

logger.basicConfig(level=logger.INFO)

class File_Distributor:
    def __init__(self):
        self.config             = Config()
        self.hd1_base_location  = self.config.hd1_location
        self.hd2_base_location  = self.config.hd2_location
        self.hd3_base_location  = self.config.hd3_location
        self.zip_folder         = os.path.join(os.getcwd(),"zip_folder")
        self.storage            = Storage()

        folder_delete_all(self.zip_folder)
        create_folder(self.zip_folder)

    # def get_hd1_files(self,num_of_files):
    #     try:
    #         list=[]
    #         count=0
    #         for folderName, subfolders, filenames in os.walk(self.hd1_base_location):
    #             for filename in filenames:
    #                     self.hd1_path =  os.path.join(folderName, filename)
    #                     if os.path.isfile(self.hd1_path):
    #                         list.append(self.hd1_path)
    #                         count=count+1
    #                     if count == num_of_files :
    #                         break
    #             if count == num_of_files:
    #                 break
    #         target_file_path=self.prepare_zip(list,"hd1.zip")
    #         return target_file_path
    #
    #     except Exception as error:
    #         logger.error(f"File_Distributor: get_hd1_files : {error}")
    #         raise error

    # def get_hd3_files(self, num_of_files):
    #     try:
    #         list = []
    #         count = 0
    #         for folderName, subfolders, filenames in os.walk(self.hd3_base_location):
    #             for filename in filenames:
    #                 self.hd3_path = os.path.join(folderName, filename)
    #                 if os.path.isfile(self.hd3_path):
    #                     list.append(self.hd3_path)
    #                     count = count + 1
    #                 if count == num_of_files:
    #                     break
    #             if count == num_of_files:
    #                 break
    #         target_file_path=self.prepare_zip(list,"hd3.zip")
    #         return target_file_path
    #
    #     except Exception as error:
    #         logger.error(f"File_Distributor: get_hd3_files : {error}")
    #         raise error

    def get_hd2_status(self):
        try:
            base_path = self.storage.hd2_status()

            if not os.listdir(base_path) :
                return -1

            target_file_path = self.prepare_zip(base_path, "hd2_status_files.zip")
            return target_file_path
        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_status : {error}")
            raise error

    def get_hd2_data(self, num_of_files):
        try:
            base_path = self.storage.hd2_data()

            if not os.listdir(base_path):
                return -1

            list = []
            if num_of_files == -1:
                for folder in os.listdir(base_path):
                    list.append(os.path.join(base_path, folder))
            else:
                count = 0
                for folder in os.listdir(base_path):
                    list.append(os.path.join(base_path,folder))
                    count=count+1
                    if count == num_of_files:
                        break

            target_file_path = self.prepare_hd2_hash_folder_zip(list,"hd2_data_files.zip")
            return target_file_path

        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_data : {error}")
            raise error

    def get_hd2_processed(self, num_of_files):
        try:
            base_path = self.storage.hd2_processed()

            if not os.listdir(base_path):
                return -1

            list  = []
            if num_of_files == -1:
                for folder in os.listdir(base_path):
                    list.append(os.path.join(base_path, folder))
            else:
                count = 0
                for folder in os.listdir(base_path):
                    list.append(os.path.join(base_path, folder))
                    count = count + 1
                    if count == num_of_files:
                        break

            target_file_path = self.prepare_hd2_hash_folder_zip(list, "hd2_processed_files.zip")
            return target_file_path

        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_processed : {error}")
            raise error

    def prepare_hd2_hash_folder_zip(self,path_list, zip_name):
        try:
            self.temp_folder = temp_folder()

            for hash_folder_path in path_list:
                name = ntpath.basename(hash_folder_path)
                dst_path = os.path.join(self.temp_folder, name)

                if os.path.isdir(hash_folder_path):
                    folder_copy(hash_folder_path, dst_path)

                    hd2_source_file = os.path.join(dst_path, "source")
                    if os.path.isfile(hd2_source_file):
                        file_delete(hd2_source_file)

            target_file_path = os.path.join(self.zip_folder, zip_name)
            zip_files(self.temp_folder, file_pattern='*.*', target_file = target_file_path)
            folder_delete_all(self.temp_folder)

            return target_file_path

        except Exception as error:
            logger.error(f"File_Distributor: prepare_zip : {error}")
            raise error

    def prepare_zip(self, path, zip_name):
        try:
            self.temp_folder = temp_folder()
            dst_path = os.path.join(self.temp_folder, ntpath.basename(path))

            if os.path.isfile(path):
                file_copy(path, dst_path)
            elif os.path.isdir(path):
                folder_copy(path, dst_path)

            target_file_path = os.path.join(self.zip_folder, zip_name)

            zip_files(self.temp_folder, file_pattern='*.*', target_file = target_file_path)

            folder_delete_all(self.temp_folder)

            return target_file_path

        except Exception as error:
            logger.error(f"File_Distributor: prepare_zip : {error}")
            raise error

