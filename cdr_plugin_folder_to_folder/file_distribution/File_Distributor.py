import os
from cdr_plugin_folder_to_folder.common_settings.Config import Config

import logging as logger
logger.basicConfig(level=logger.INFO)

class File_Distributor:
    def __init__(self):

        self.config             = Config().load_values()
        self.hd1_base_location  = self.config.hd1_location
        self.hd2_base_location  = self.config.hd2_location
        self.hd3_base_location  = self.config.hd3_location

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
                            return list
            return list

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
                        return list
            return list

        except Exception as error:
            logger.error(f"File_Distributor: get_hd3_files : {error}")
            raise error

    def get_hd2_metadata_files(self, num_of_files):
        try:
            list = []
            count = 0
            for folder in os.listdir(os.path.join(self.hd2_base_location,"data")):
                list.append(os.path.join(folder,"metadata.json"))
                count=count+1
                if count== num_of_files:
                    return list
            return list

        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_metadata_files : {error}")
            raise error

    def get_hd2_source_files(self, num_of_files):
        try:
            list = []
            count = 0
            for folder in os.listdir(os.path.join(self.hd2_base_location,"data")):
                list.append(os.path.join(folder,"source"))
                count=count+1
                if count == num_of_files:
                    return list
            return list
        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_source_files : {error}")
            raise error

    def get_hd2_hash_folder_list(self,num_of_files):

        try:
            list = []
            count = 0
            for folder in os.listdir(os.path.join(self.hd2_base_location,"data")):
                list.append(folder)
                count=count+1
                if count == num_of_files:
                    return list
            return list
        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_hash_folder_list : {error}")
            raise error

    def get_hd2_report_files(self,num_of_files):
        try:
            list = []
            count = 0
            for folder in os.listdir(os.path.join(self.hd2_base_location,"data")):
                list.append(os.path.join(folder,"report.json"))
                count=count+1
                if count == num_of_files:
                    return list
            return list
        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_report_files : {error}")
            raise error

    def get_hd2_status_hash_file(self):
        try:
            list = []
            list.append(os.path.join(os.path.join(self.hd2_base_location,"status"),"hash.json"))
            return list
        except Exception as error:
            logger.error(f"File_Distributor: get_hd2_status_hash_file : {error}")
            raise error

    def download_file(self,file_path):
        pass











