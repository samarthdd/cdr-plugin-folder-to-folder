import hashlib

import logging as logger
logger.basicConfig(level=logger.INFO)

class Metadata_Service:

    def get_metadata(self,file_path,hd1_path):
        # Create metadata json
        try:
            self.file_path=file_path
            metadata={}
            metadata["file_name"]           = self.file_path.split("/")[-1]
            metadata["original_file_paths"] = hd1_path
            metadata["original_hash"]       = self.get_hash(self.file_path)
            metadata["evidence_file_paths"] = None
            metadata["rebuild_status"]      = None
            metadata["xml_report_status"]   = None
            metadata["target_path"]         = None

            return metadata
        except Exception as error:
            logger.error(f"PreProcessor: get_metadata : {error}")

    def get_hash(self,file_path):
        # Convert filecontent to hash
        try:
            f            = open(file_path, mode='rb')
            file_content = f.read()
            sha256_hash  = hashlib.sha256(file_content).hexdigest()
            f.close()
            return sha256_hash
        except Exception as error:
            logger.error(f"PreProcessor: get_hash : {error}")

    def get_json_field(self,field_name,file_path):
        pass
    def set_json_field(self,field_name,file_path):
        pass










