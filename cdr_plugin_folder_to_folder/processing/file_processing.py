import sys
import json
import requests
import ntpath
import os.path

sys.path.insert(1, '../common_settings')
from config_params import Config
sys.path.insert(1, '../utils')
from file_service import FileService

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
            print("ERROR: {}".format(e))
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
            print("Cannot get xml report for {}", source_path)
            return

        report_folder = os.path.join(Config.hd2_location,"reports")
        FileService.create_folder(report_folder)

        report_file_folder = os.path.join(report_folder,hash)
        FileService.create_folder(report_file_folder)

        FileService.wrtie_file(report_file_folder,"report.xml",xmlreport)
        
    @staticmethod
    def processDirectory (dir):

        hash = ntpath.basename(dir)
        if len(hash) != 64:
            print("Enexpected hash length for {}", dir)
            return

        source_path = os.path.join(dir, "source")
        if not (FileService.file_exist(source_path)):
            print("File does not exist {}", source_path)
            return

        encodedFile = FileService.base64encode(source_path)
        if not encodedFile:
            print("Cannot encode {}", source_path)
            return

        FileProcessing.create_report(hash, encodedFile)

    @staticmethod
    def main(argv):
        f = open("base64.sample", "r")
        base64_value = f.read()

        #result = FileProcessing.filetypedetection(base64_value)
        #print(result)

        #result = FileProcessing.analyse(base64_value)
        #print(result)
        
        #result = FileProcessing.rebuild(base64_value)
        #print(result)

        #file = open("sample.pdf", "wb")
        #file.write(FileService.base64decode(result))
        #file.close()

        FileProcessing.processDirectory("C:\\gw_test\\hd2\\data\\32823a0dbe4dd137873cd286a592436ef738b10ce16e746a1ec64fb07c027615")

if __name__ == "__main__":
    FileProcessing.main(sys.argv[1:])
