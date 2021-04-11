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
    def base64request(endpoint, api_route, base64enc_file):
        try:
            url = endpoint + "/" + api_route

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
    def xmlreport_request(endpoint, fileID):
        try:
            url = endpoint + "/api/Analyse/xmlreport?fileId=" + fileID

            payload = ""
            headers = {
                'Content-Type': 'application/octet-stream'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            return response.text

        except Exception as e:
            raise ValueError(str(e))

    @staticmethod
    def analyse (endpoint, base64enc_file):
        return File_Processing.base64request(endpoint, "api/Analyse/base64", base64enc_file)

    @staticmethod
    def rebuild (endpoint, base64enc_file):
        return File_Processing.base64request(endpoint, "api/rebuild/base64", base64enc_file)

    @staticmethod
    def filetypedetection (endpoint, base64enc_file):
        return File_Processing.base64request(endpoint, "api/FileTypeDetection/base64", base64enc_file)

    @staticmethod
    def get_xmlreport(endpoint, fileId, dir):
        xmlreport = File_Processing.xmlreport_request(endpoint, fileId)
        if not xmlreport:
            raise ValueError('Failed to obtain the XML report')

        json_obj = xmltodict.parse(xmlreport)
        json_save_file_pretty(json_obj, os.path.join(dir, "report.json"))

    @staticmethod
    def do_rebuild(endpoint, hash, encodedFile, dir):
        response = File_Processing.rebuild(endpoint, encodedFile)
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
            File_Processing.get_xmlreport(endpoint, headers[fileIdKey], dir)
        else:
            raise ValueError("No X-Adaptation-File-Id header found in the response")

    @staticmethod
    def processDirectory (endpoint, dir):

        hash = ntpath.basename(dir)
        if len(hash) != 64:
            raise ValueError("Unexpected hash length")

        if not File_Processing.meta_service.is_initial_status(dir):
            return

        File_Processing.meta_service.set_status_inprogress(dir)

        source_path = os.path.join(dir, "source")
        if not (FileService.file_exist(source_path)):
            raise ValueError("File does not exist")

        metadata_file_path = os.path.join(dir, Metadata_Service.METADATA_FILE_NAME)
        if not (FileService.file_exist(metadata_file_path)):
            raise ValueError("The metadate.json file does not exist")

        encodedFile = FileService.base64encode(source_path)
        if not encodedFile:
            raise ValueError("Failed to encode the file")

        File_Processing.do_rebuild(endpoint, hash, encodedFile, dir)

        File_Processing.meta_service.set_status_comleted(dir)

