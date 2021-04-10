import os
from cdr_plugin_folder_to_folder.common_settings.Config import Config

import logging as logger
from os import environ
logger.basicConfig(level=logger.INFO)
import dotenv

class Configure_Env:
    def __init__(self):
        pass

    def configure(self, hd1_path=None, hd2_path=None, hd3_path=None,gw_address=None, gw_port=None):
        try:
            dotenv_file = dotenv.find_dotenv()
            if hd1_path:
                if os.path.exists(hd1_path):
                    environ['HD1_LOCATION'] = hd1_path
                    dotenv.set_key(dotenv_file, "HD1_LOCATION", os.environ["HD1_LOCATION"])
                else:
                    return 0
            if hd2_path:
                if os.path.exists(hd1_path):
                    environ['HD2_LOCATION'] = hd2_path
                    dotenv.set_key(dotenv_file, "HD2_LOCATION", os.environ["HD2_LOCATION"])
                else:
                    return 0
            if hd3_path:
                if os.path.exists(hd1_path):
                    environ['HD3_LOCATION'] = hd3_path
                    dotenv.set_key(dotenv_file, "HD3_LOCATION", os.environ["HD3_LOCATION"])
                else:
                    return 0
            if gw_address:
                environ['GW_SDK_ADDRESS'] = gw_address
                dotenv.set_key(dotenv_file, "GW_SDK_ADDRESS", os.environ["GW_SDK_ADDRESS"])
            if gw_port:
                if int(gw_port):
                    environ['GW_SDK_PORT'] = gw_port
                    dotenv.set_key(dotenv_file, "GW_SDK_PORT", os.environ["GW_SDK_PORT"])
                else:
                    return 0

            return self.env_details()

        except Exception as error:
            raise ValueError(str(error))

    def env_details(self):
        try:
            return {
                "hd1_path": environ.get('HD1_LOCATION'),
                "hd2_path": environ.get('HD2_LOCATION'),
                "hd3_path": environ.get('HD3_LOCATION'),
                "gw_address": environ.get('GW_SDK_ADDRESS'),
                "gw_port": environ.get('GW_SDK_PORT'),
            }
        except Exception as error:
            raise error


    def configure_endpoints(self, endpoint_string):
        try:
            dotenv_file = dotenv.find_dotenv()
            environ['ENDPOINTS'] = endpoint_string
            logger.info(f"ENDPOINTS : {environ['ENDPOINTS']}")
            dotenv.set_key(dotenv_file, "ENDPOINTS", os.environ["ENDPOINTS"])

            return environ['ENDPOINTS']

        except Exception as error:
            raise error






