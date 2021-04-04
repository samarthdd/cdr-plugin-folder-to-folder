import os
#import logging
import sys, getopt
#import json
from dotenv import load_dotenv

DEFAULT_HD1_LOCATION   = "./test_data/hd1"
DEFAULT_HD2_LOCATION   = "./test_data/hd2"
DEFAULT_HD3_LOCATION   = "./test_data/hd3"
DEFAULT_GW_SDK_ADDRESS = "91.109.26.86"
DEFAULT_GW_SDK_PORT    = "8080"

class Config(object):
    load_dotenv()       # Load configuration from .env file that should exist in the root of the repo
    try:
        hd1_location    = os.getenv("HD1_LOCATION"   , DEFAULT_HD1_LOCATION)
        hd2_location    = os.getenv("HD2_LOCATION"   , DEFAULT_HD2_LOCATION)
        hd3_location    = os.getenv("HD3_LOCATION"   , DEFAULT_HD3_LOCATION)
        gw_sdk_address  = os.getenv("GW_SDK_ADDRESS" , DEFAULT_GW_SDK_ADDRESS)
        gw_sdk_port     = int(os.getenv("GW_SDK_PORT", DEFAULT_GW_SDK_PORT))

        temp_folder = "../tmp"
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        data_folder = os.path.join(hd2_location,"data")
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        status_folder = os.path.join(hd2_location,"status")
        if not os.path.exists(status_folder):
            os.makedirs(status_folder)

    except Exception as e:
        print(
            "Please create config.env file similar to config.env.sample")
        print(str(e))
        raise

    #The function below is to verify that config params are obtained from config.env
    @staticmethod
    def main(argv):
        print("HD1            - {}".format(Config.hd1_location))
        print("HD2            - {}".format(Config.hd2_location))
        print("HD3            - {}".format(Config.hd3_location))    
        print("GW SDK Address - {}".format(Config.gw_sdk_address))    
        print("GW SDK Port    - {}".format(Config.gw_sdk_port))    

if __name__ == "__main__":
    Config.main(sys.argv[1:])