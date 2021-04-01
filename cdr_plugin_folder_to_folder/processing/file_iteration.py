import sys
sys.path.insert(1, '../common_settings')
from config_params import Config

class FileOperations(object):

    @staticmethod
    def main(argv):
        print("HD1            - {}".format(Config.hd1_location))
        print("HD2            - {}".format(Config.hd2_location))
        print("HD3            - {}".format(Config.hd3_location))    
        print("GW SDK Address - {}".format(Config.gw_sdk_address))    
        print("GW SDK Port    - {}".format(Config.gw_sdk_port))    

if __name__ == "__main__":
    FileOperations.main(sys.argv[1:])