import sys
import json
import requests
import ntpath
import os.path
import xmltodict

from osbot_utils.utils.Files import folder_create
from osbot_utils.utils.Json import json_save_file_pretty

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.utils.file_utils import FileService
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service

class File_Processing(object):

    config = Config().load_values()
    meta_service = Metadata_Service()

    @staticmethod
    def base64request(endpoint, base64enc_file):
        try:
            url = "http://" + File_Processing.config.gw_sdk_address + ":" \
                + str(File_Processing.config.gw_sdk_port) + "/" + endpoint

            payload = json.dumps({
              "Base64": base64enc_file
            })

            headers = {
              'Content-Type': 'application/json'
            }

            return requests.request("POST", url, headers=headers, data=payload)
     
        except Exception as e:
            raise ValueError(str(e))

    @staticmethod
    def xmlreport_request(fileID):
        try:
            url = "http://" + File_Processing.config.gw_sdk_address \
                + ":" + str(File_Processing.config.gw_sdk_port) \
                + "/api/Analyse/xmlreport?fileId=" + fileID

            payload = ""
            headers = {
                'Content-Type': 'application/octet-stream'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            return response.text

        except Exception as e:
            raise ValueError(str(e))

    @staticmethod
    def analyse (base64enc_file):
        return File_Processing.base64request("api/Analyse/base64", base64enc_file)

    @staticmethod
    def rebuild (base64enc_file):
        return File_Processing.base64request("api/rebuild/base64", base64enc_file)

    @staticmethod
    def filetypedetection (base64enc_file):
        return File_Processing.base64request("api/FileTypeDetection/base64", base64enc_file)

    @staticmethod
    def get_xmlreport(hash, fileId, dir):
        xmlreport = File_Processing.xmlreport_request(fileId)
        if not xmlreport:
            raise ValueError('Failed to create the XML report')

        json_obj = xmltodict.parse(xmlreport)
        json_save_file_pretty(json_obj, os.path.join(dir, "report.json"))

    @staticmethod
    def do_rebuild(hash, encodedFile, dir):
        response = File_Processing.rebuild(encodedFile)
        result = response.text
        if not result:
            raise ValueError('Failed to rebuild the file')

        processed_path = File_Processing.meta_service.get_processed_file_path(dir)

        dirname = ntpath.dirname(processed_path)
        basename = ntpath.basename(processed_path)
        folder_create(dirname)

        decoded = FileService.base64decode(result)

        # Save to HD3
        if decoded:
            FileService.wrtie_binary_file(dirname, basename, decoded)
        else:
            FileService.wrtie_file(dirname, basename + ".html", result)

        headers = response.headers
        fileIdKey = "X-Adaptation-File-Id"

        # get XML report
        if fileIdKey in headers:
            File_Processing.get_xmlreport(hash, headers[fileIdKey], dir)

    @staticmethod
    def processDirectory (dir):

        hash = ntpath.basename(dir)
        if len(hash) != 64:
            raise ValueError("Unexpected hash length")

        if not File_Processing.meta_service.is_initial_status(dir):
            return

        File_Processing.meta_service.set_status_inprogress(dir)

        source_path = os.path.join(dir, "source")
        if not (FileService.file_exist(source_path)):
            print("File does not exist: ", source_path)
            return False

        metadata_file_path = os.path.join(dir, Metadata_Service.METADATA_FILE_NAME)
        if not (FileService.file_exist(metadata_file_path)):
            raise ValueError("The metadate.json file does not exist")

        encodedFile = FileService.base64encode(source_path)
        if not encodedFile:
            raise ValueError("Failed to encode the file")

        File_Processing.do_rebuild(hash, encodedFile, dir)

        File_Processing.meta_service.set_status_comleted(dir)

    @staticmethod
    def main(argv):
        File_Processing.processDirectory("C:\\gw_test\\hd2\\data\\32823a0dbe4dd137873cd286a592436ef738b10ce16e746a1ec64fb07c027615")

if __name__ == "__main__":
    File_Processing.main(sys.argv[1:])
