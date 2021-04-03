import sys
import json
import requests
import ntpath
import os.path

sys.path.insert(1, '../common_settings')
from config_params import Config
sys.path.insert(1, '../utils')
from file_utils import FileService

class FileProcessing(object):

    @staticmethod
    def base64request(endpoint, base64enc_file):
        try:
            url = "http://" + Config.gw_sdk_address + ":" + str(Config.gw_sdk_port) + "/" + endpoint

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
        return FileProcessing.base64request("api/Analyse/base64",base64enc_file)

    @staticmethod
    def rebuild (base64enc_file):
        return FileProcessing.base64request("api/rebuild/base64", base64enc_file)

    @staticmethod
    def filetypedetection (base64enc_file):
        return FileProcessing.base64request("api/FileTypeDetection/base64",base64enc_file)

    @staticmethod
    def create_report(hash, encodedFile):
        xmlreport = FileProcessing.analyse(encodedFile)
        if not xmlreport:
            print("Cannot get xml report")
            return

        report_folder = os.path.join(Config.hd2_location,"reports")
        FileService.create_folder(report_folder)

        report_file_folder = os.path.join(report_folder,hash)
        FileService.create_folder(report_file_folder)

        FileService.wrtie_file(report_file_folder,"report.xml",xmlreport)

    @staticmethod
    def do_rebuild(hash, encodedFile):
        result = FileProcessing.rebuild(encodedFile)
        if not result:
            print("Cannot rebuild file")
            return

        rebuild_folder = os.path.join(Config.hd2_location,"processed")
        FileService.create_folder(rebuild_folder)

        rebuild_file_folder = os.path.join(rebuild_folder,hash)
        FileService.create_folder(rebuild_file_folder)

        decoded = FileService.base64decode(result)

        if decoded:
            FileService.wrtie_binary_file(rebuild_file_folder, "rebuild", decoded)
        else:
            FileService.wrtie_file(rebuild_file_folder, "failed.html", result)

    @staticmethod
    def processDirectory (dir):

        hash = ntpath.basename(dir)
        if len(hash) != 64:
            print("Enexpected hash length for: ", dir)
            return

        source_path = os.path.join(dir, "source")
        if not (FileService.file_exist(source_path)):
            print("File does not exist: ", source_path)
            return

        metadata_file_path = os.path.join(dir, "metadata.json")
        if not (FileService.file_exist(metadata_file_path)):
            print("File does not exist: ", metadata_file_path)
            return

        #metadata_file = open(metadata_file_path)
        #metadata = json.load(metadata_file)
        #metadata_file.close()

        encodedFile = FileService.base64encode(source_path)
        if not encodedFile:
            print("Cannot encode: ", source_path)
            return

        FileProcessing.create_report(hash, encodedFile)

        FileProcessing.do_rebuild(hash, encodedFile)

    @staticmethod
    def main(argv):
        FileProcessing.processDirectory("C:\\gw_test\\hd2\\data\\32823a0dbe4dd137873cd286a592436ef738b10ce16e746a1ec64fb07c027615")

if __name__ == "__main__":
    FileProcessing.main(sys.argv[1:])
