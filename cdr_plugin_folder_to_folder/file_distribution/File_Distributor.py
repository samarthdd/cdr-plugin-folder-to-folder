import os
from cdr_plugin_folder_to_folder.common_settings.Config import Config
import ntpath
import logging as logger
from os import environ
from osbot_utils.utils.Files import folder_exists, zip_files,temp_folder, file_exists, folder_temp, folder_delete_all, temp_file, \
    file_copy,file_contents,folder_copy,create_folder

logger.basicConfig(level=logger.INFO)

class File_Distributor:
    def __init__(self):
        self.config             = Config().load_values()
        self.hd1_base_location  = self.config.hd1_location
        self.hd2_base_location  = self.config.hd2_location
        self.hd3_base_location  = self.config.hd3_location
        self.zip_folder         = os.path.join(os.getcwd(),"zip_folder")

        folder_delete_all(self.zip_folder)
        create_folder(self.zip_folder)

    def get_hd1_files(self,num_of_files):
        try:
            list=[]
            count=0
            for folderName, subfolders, filenames in os.walk(self.hd1_base_location):
                for filename in filenames:
                        self.hd1_path =  os.path.join(folderName, filename)
                        if os.path.isfile(self.hd1_path):
                            list.append(self.hd1_path)
                            count=count+1
                        if count == num_of_files :
                            break
                if count == num_of_files:
                    break
            target_file_path=self.prepare_zip(list,"hd1.zip")
            return target_file_path

        except Exception as error:
            logger.error(f"File_Distributor: get_hd1_files : {error}")
            raise error

    def get_hd3_files(self, num_of_files):
        try:
            list = []
            count = 0
            for folderName, subfolders, filenames in os.walk(self.hd3_base_location):
                for filename in filenames:
                    self.hd3_path = os.path.join(folderName, filename)
                    if os.path.isfile(self.hd3_path):
                        list.append(self.hd3_path)
                        count = count + 1
                    if count == num_of_files:
                        break
                if count == num_of_files:
                    break
            target_file_path=self.prepare_zip(list,"hd3.zip")
            return target_file_path

        except Exception as error:
            logger.error(f"File_Distributor: get_hd3_files : {error}")
            raise error

    def get_hd2_metadata_files(self, num_of_files):
        try:
            list = []
            count = 0
            base_path=os.path.join(self.hd2_base_location,"data")
            for folder in os.listdir(base_path):
                list.append(os.path.join(base_path,folder,"metadata.json"))
                count=count+1
                if count== num_of_files:
                    break
            target_file_path = self.prepare_zip(list,"hd2_metadata.zip")
            return target_file_path

        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_metadata_files : {error}")
            raise error

    def get_hd2_source_files(self, num_of_files):
        try:
            list = []
            count = 0
            base_path = os.path.join(self.hd2_base_location, "data")
            for folder in os.listdir(base_path):
                list.append(os.path.join(base_path,folder,"source"))
                count=count+1
                if count == num_of_files:
                    break
            target_file_path = self.prepare_zip(list,"hd2_source.zip")
            return target_file_path
        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_source_files : {error}")
            raise error

    def get_hd2_hash_folder_list(self,num_of_files):

        try:
            list = []
            count = 0
            base_path = os.path.join(self.hd2_base_location, "data")
            for folder in os.listdir(base_path):
                list.append(os.path.join(base_path,folder))
                count=count+1
                if count == num_of_files:
                    break
            target_file_path = self.prepare_zip(list,"hd2_hash_folder.zip")
            return target_file_path
        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_hash_folder_list : {error}")
            raise error

    def get_hd2_report_files(self,num_of_files):
        try:
            list = []
            count = 0
            base_path = os.path.join(self.hd2_base_location, "data")
            for folder in os.listdir(base_path):
                list.append(os.path.join(base_path,folder,"report.json"))
                count=count+1
                if count == num_of_files:
                    break
            target_file_path = self.prepare_zip(list,"hd2_report_json.zip")
            return target_file_path
        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_report_files : {error}")
            raise error

    def get_hd2_status_hash_file(self):
        try:
            file_path=os.path.join(os.path.join(self.hd2_base_location,"status"),"hash.json")
            return file_path
        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_status_hash_file : {error}")
            raise error

    def prepare_zip(self,file_path_list,zip_name):
        try:
            self.temp_folder = temp_folder()
            for src_path in file_path_list:
                name = ntpath.basename(src_path)
                if len(name.split("."))==1:
                    name=name+".txt"
                dst_path = os.path.join(self.temp_folder, name)
                if os.path.isfile(src_path):
                    file_copy(src_path, dst_path)
                elif os.path.isdir(src_path):
                    folder_copy(src_path, dst_path)

            target_file_path = os.path.join(self.zip_folder, zip_name)
            zip_files(self.temp_folder, file_pattern='*.*', target_file=target_file_path)
            folder_delete_all(self.temp_folder)

            return target_file_path

        except Exception as error:
            logger.error(f"File_Distributor: prepare_zip : {error}")
            raise error