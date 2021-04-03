import hashlib

import logging as logger

from osbot_utils.utils.Files import file_sha256, file_name

logger.basicConfig(level=logger.INFO)

class Metadata_Service:

    def __init__(self):
        self.file_path = None

    def get_metadata(self, file_path, hd1_path):
        # Create metadata json
        self.file_path=file_path
        metadata = {"file_name"          : file_name(self.file_path)     ,
                    "original_file_paths": hd1_path                      ,  # todo: DC: check why we need this (since I think this is part of the file_path variable)
                    "original_hash"      : self.get_hash(self.file_path) ,
                    "evidence_file_paths": None                          ,
                    "rebuild_status"     : None                          ,
                    "xml_report_status"  : None                          ,
                    "target_path"        : None                          }
        return metadata

    def get_hash(self,file_path):
        return file_sha256(file_path)

    def get_json_field(self,field_name,file_path):
        pass

    def set_json_field(self,field_name,file_path):
        pass










