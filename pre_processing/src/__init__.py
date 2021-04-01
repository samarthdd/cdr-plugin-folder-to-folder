import hashlib
import os
import sys

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
            metadata_content=self.meta_service.get_metadata(file_path=self.current_path)

            # Get SHA 256 hash
            self.hash = metadata_content["original_hash"]

            # Create basefolder
            self.base_folder=os.path.join(self.temp_folder,self.hash)
            self.file_service.create_folder(folder_name=self.base_folder)

            # Store metadata
            self.file_service.wrtie_file(folder=self.base_folder,file_name="metadata.json",content=metadata_content)

            #Rename and Move original file to hash folder
            self.name="source"
            self.file_service.move_file(self.current_path,os.path.join(self.base_folder, self.name))

            # Store hash folder to HD2
            self.destination=os.path.join(self.target, self.hash)
            if not os.path.exists(self.destination):
                self.file_service.copy_folder(self.base_folder,self.destination)
            else:
                # todo : Update HD2 metadata with source paths
                pass

            # Delete temp hash folder
            self.file_service.delete_folder(self.base_folder)

        except Exception as error:
            logger.error(f"PreProcessor: process : {error}")

    def get_hash(self,file_path):
        # Convert filecontent to hash
        try:
            f = open(file_path, mode='rb')
            file_content = f.read()
            sha256_hash = hashlib.sha256(file_content).hexdigest()
            f.close()
            return sha256_hash
        except Exception as error:
            logger.error(f"PreProcessor: get_hash : {error}")

    def get_metadata(self):
        # Create metadata json
        try:
            metadata={}
            metadata["file_name"]=self.file_name
            metadata["original_file_paths"] = self.file_path
            metadata["original_hash"] = self.hash
            metadata["evidence_file_paths"]=None
            metadata["rebuild_status"] = None
            metadata["xml_report_status"] = None
            metadata["target_path"] = None

            return metadata
        except Exception as error:
            logger.error(f"PreProcessor: get_metadata : {error}")

    def update_hd2_metadata(self):
        # Update HD2 metadata with source paths
        pass
    def update_status(self):
        # update original_hash.json
        pass

if __name__ == '__main__' :
    pre_processor=PreProcessor()
    pre_processor.process_files()
