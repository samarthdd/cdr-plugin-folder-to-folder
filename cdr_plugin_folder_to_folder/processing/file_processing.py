import sys
sys.path.insert(1, '../common_settings')
from config_params import Config
import requests
import json

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
    def main(argv):
        f = open("base64.sample", "r")
        base64_value = f.read()

        result = FileProcessing.filetypedetection(base64_value)
        print(result)

        result = FileProcessing.analyse(base64_value)
        #report_path = os.path.join(Current.temp_folder, "report.xml")
        print(result)
        
        result = FileProcessing.rebuild(base64_value)
        print(result)

if __name__ == "__main__":
    FileProcessing.main(sys.argv[1:])
