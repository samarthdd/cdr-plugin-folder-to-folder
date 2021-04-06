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

class File_Processing(object):                                       # todo: add Unit Tests to this class

    @staticmethod
    def base64request(endpoint, base64enc_file):
        config = Config().load_values()                             # todo refactor out of this method (since this should be loaded once, not everytime it is executed)
        try:
            url = "http://" + config.gw_sdk_address + ":" + str(config.gw_sdk_port) + "/" + endpoint

            payload = json.dumps({
              "Base64": base64enc_file
            })

            headers = {
              'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            return response.text
     
        except Exception as e:
            print("ERROR: ".format(e))
            return ""

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
    def create_report(hash, encodedFile):
        config = Config().load_values()                     # todo refactor out of this method (since this should be loaded once, not everytime it is executed)
        xmlreport = File_Processing.analyse(encodedFile)
        if not xmlreport:
            print("Cannot get xml report")
            return

        report_folder = os.path.join(config.hd2_location,"data")     # todo: this should not be calculated here
        folder_create(report_folder)                                    # todo: this folder should not be created here

        report_file_folder = os.path.join(report_folder,hash)           # todo: this should not be calculated here
        folder_create(report_file_folder)                               # todo: this folder should not be created here

        json_obj = xmltodict.parse(xmlreport)

        json_save_file_pretty(json_obj, os.path.join(report_file_folder, "report.json"))

    @staticmethod
    def do_rebuild(hash, encodedFile, processed_path):
        result = File_Processing.rebuild(encodedFile)
        if not result:
            print("Cannot rebuild file")
            return

        dirname = ntpath.dirname(processed_path)
        basename = ntpath.basename(processed_path)
        folder_create(dirname)

        decoded = FileService.base64decode(result)

        # Save to HD3
        if decoded:
            FileService.wrtie_binary_file(dirname, basename, decoded)
        else:
            FileService.wrtie_file(dirname, basename + ".html", result)

    @staticmethod
    def processDirectory (dir):

        hash = ntpath.basename(dir)
        if len(hash) != 64:
            print("Enexpected hash length for: ", dir)
            return False

        meta_service = Metadata_Service()
        if not meta_service.is_initial_status(dir):
            return False

        meta_service.set_status_inprogress(dir)

        source_path = os.path.join(dir, "source")
        if not (FileService.file_exist(source_path)):
            print("File does not exist: ", source_path)
            return False

        metadata_file_path = os.path.join(dir, Metadata_Service.METADATA_FILE_NAME)
        if not (FileService.file_exist(metadata_file_path)):
            print("File does not exist: ", metadata_file_path)
            return False

        encodedFile = FileService.base64encode(source_path)
        if not encodedFile:
            print("Cannot encode: ", source_path)
            return False

        processed_path = meta_service.get_processed_file_path(dir)

        File_Processing.create_report(hash, encodedFile)
        File_Processing.do_rebuild(hash, encodedFile, processed_path)

        meta_service.set_status_comleted(dir)

        return True

    @staticmethod
    def main(argv):
        File_Processing.processDirectory("C:\\gw_test\\hd2\\data\\32823a0dbe4dd137873cd286a592436ef738b10ce16e746a1ec64fb07c027615")

if __name__ == "__main__":
    File_Processing.main(sys.argv[1:])
