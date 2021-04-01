import os
#import logging
import sys, getopt
#import json
from dotenv import load_dotenv

class Config(object):
    # Load configuration
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(BASEDIR, 'config.env'), override=True)
    try:

        hd1_location = os.getenv("HD1_LOCATION")
        hd2_location = os.getenv("HD2_LOCATION")
        hd3_location = os.getenv("HD3_LOCATION")
        gw_sdk_address = os.getenv("GW_SDK_ADDRESS")
        gw_sdk_port = int(os.getenv("GW_SDK_PORT",8080))

        temp_folder = "./tmp"
        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")

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