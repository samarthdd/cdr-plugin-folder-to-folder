import json

from cdr_plugin_folder_to_folder.common_settings.Config import Config

from os import environ,path
import dotenv

import logging as logger

from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing

logger.basicConfig(level=logger.INFO)

class Configure_Env:
    def __init__(self):
        Setup_Testing().set_test_root_dir()
        dotenv_file = dotenv.find_dotenv()
        if not dotenv_file:
            with open("./.env", "w"):
                pass

    def configure(self, hd1_path=None, hd2_path=None, hd3_path=None):
        try:
            dotenv_file = dotenv.find_dotenv()
            if hd1_path:
                if path.exists(hd1_path):
                    environ['HD1_LOCATION'] = hd1_path
                    dotenv.set_key(dotenv_file, "HD1_LOCATION", environ["HD1_LOCATION"])
                else:
                    return 0
            if hd2_path:
                if path.exists(hd1_path):
                    environ['HD2_LOCATION'] = hd2_path
                    dotenv.set_key(dotenv_file, "HD2_LOCATION", environ["HD2_LOCATION"])
                else:
                    return 0
            if hd3_path:
                if path.exists(hd1_path):
                    environ['HD3_LOCATION'] = hd3_path
                    dotenv.set_key(dotenv_file, "HD3_LOCATION", environ["HD3_LOCATION"])
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
                "hd3_path": environ.get('HD3_LOCATION')
            }
        except Exception as error:
            raise error


    def configure_endpoints(self, endpoint_string):
        try:
            dotenv_file = dotenv.find_dotenv()
            environ['ENDPOINTS'] = endpoint_string
            logger.info(f"ENDPOINTS : {environ['ENDPOINTS']}")
            dotenv.set_key(dotenv_file, "ENDPOINTS", environ["ENDPOINTS"])

            return json.loads(environ['ENDPOINTS'])

        except Exception as error:
            raise error






