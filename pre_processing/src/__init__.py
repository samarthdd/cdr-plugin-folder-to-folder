import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from common_settings.config_params import Config
from src.utils.file_service import FileService

from metadata.src.metadata_service import MetadataService

import logging as logger
logger.basicConfig(level=logger.INFO)

class PreProcessor:
    def __init__(self):
        self.filename      =  None
        self.hash          =  None
        self.file_path     =  None

        self.temp_folder   =  Config.temp_folder
        self.target        =  os.path.join(Config.hd2_location , "data")

        self.file_service  =  FileService()
        self.meta_service  =  MetadataService()
        self.id=0
        self.hash_json=[]

    def process_files(self):
        try:
            for folderName, subfolders, filenames in os.walk(Config.hd1_location):
                for filename in filenames:
                    self.file_path =  os.path.join(folderName, filename)
                    if os.path.isfile(self.file_path):
                        self.process(self.file_path)
        except Exception as error:
            logger.error(f"PreProcessor: process_files {error}")

    def process(self,file_path):
        try:
            self.file_path=file_path
            self.file_name = file_path.split("/")[-1]

            self.current_path = os.path.join(self.temp_folder, self.file_name)

            # Copy File
            self.file_service.copy_file(self.file_path,self.current_path)

            # Get metadata
            metadata_content=self.meta_service.get_metadata(file_path=self.current_path,hd1_path=self.file_path)

            # Get SHA 256 hash
            self.hash = metadata_content["original_hash"]

            # Create basefolder
            self.base_folder = os.path.join(self.temp_folder, self.hash)
            self.file_service.create_folder(folder_name=self.base_folder)

            # target folder
            self.destination=os.path.join(self.target, self.hash)

            # Check hash folder exists in HD2
            if not os.path.exists(self.destination):

                # Store metadata
                self.file_service.wrtie_json_file(folder=self.base_folder, file_name="metadata.json",
                                                  content=metadata_content)

                # Rename and Move original file to hash folder
                self.name = "source"
                self.file_service.move_file(self.current_path, os.path.join(self.base_folder, self.name))

                # Store hash folder to HD2
                self.file_service.copy_folder(self.base_folder,self.destination)

            else:
                # Update HD2 metadata with source paths
                self.update_hd2_metadata()
                os.remove(self.current_path)

            # Delete temp hash folder
            self.file_service.delete_folder(self.base_folder)

            self.update_status()

        except Exception as error:
            logger.error(f"PreProcessor: process : {error}")

    def update_hd2_metadata(self):
        # Update HD2 metadata with source paths
        src=os.path.join(self.destination,"metadata.json")
        dst=os.path.join(self.base_folder,"metadata.json")
        self.file_service.copy_file(src,dst)
        metadata_content=self.file_service.read_json_file(dst)
        if metadata_content["original_file_paths"] != self.file_path:
            metadata_content["original_file_paths"] = metadata_content["original_file_paths"]+ "," + self.file_path
            self.file_service.wrtie_json_file(folder=self.base_folder,file_name="metadata.json",content=metadata_content)
            self.file_service.copy_file(dst,src)

    # def update_status(self):
    #     # update original_hash.json
    #     self.jsondb = db.getDb("original_hash.json")
    #     json_data={}
    #     json_data["file_name"]=self.file_name
    #     json_data["original_hahs"]=self.hash
    #     json_data=json.dumps(json_data)
    #
    #     self.jsondb.addMany(json_data)
    def update_status(self):

        self.id=self.id+1

        json_data={}
        json_data["id"]=self.id
        json_data["file_name"]=self.file_name
        json_data["original_hahs"]=self.hash
        self.hash_json.append(json_data)
        #json_data=json.dumps(json_data)

        self.file_service.wrtie_json_file(Config.hd2_location+"/"+"status","hash.json",json.dumps(self.hash_json))





if __name__ == '__main__' :
    pre_processor=PreProcessor()
    pre_processor.process_files()
