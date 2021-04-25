import json

from cdr_plugin_folder_to_folder.common_settings.Config import Config

from os import environ,path
import dotenv

import logging as logger

from cdr_plugin_folder_to_folder.utils.Logging import log_error
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing
from urllib.parse import urljoin
import requests

logger.basicConfig(level=logger.INFO)

class Configure_Env:
    def __init__(self):
        self.config = Config()
        #dotenv_file = dotenv.find_dotenv()
        #if not dotenv_file:
        #    with open("./.env", "w"):
        #        pass

    def configure(self, hd1_path=None, hd2_path=None, hd3_path=None):
        try:
            dotenv_file = dotenv.find_dotenv()
            if hd1_path:
                if path.exists(hd1_path):
                    environ['HD1_LOCATION'] = hd1_path
                    dotenv.set_key(dotenv_file, "HD1_LOCATION", environ["HD1_LOCATION"])
                else:
                    log_error(message=f"hd1_path did not exist",data={"path": hd1_path})
                    return -1
            if hd2_path:
                if path.exists(hd2_path):
                    environ['HD2_LOCATION'] = hd2_path
                    dotenv.set_key(dotenv_file, "HD2_LOCATION", environ["HD2_LOCATION"])
                else:
                    log_error(message=f"hd2_path did not exist", data={"path": hd2_path})
                    return -1
            if hd3_path:
                if path.exists(hd3_path):
                    environ['HD3_LOCATION'] = hd3_path
                    dotenv.set_key(dotenv_file, "HD3_LOCATION", environ["HD3_LOCATION"])
                else:
                    log_error(message=f"hd3_path did not exist", data={"path": hd3_path})
                    return -1
            self.config.load_values()
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
            valid_endpoint_string=self.get_valid_endpoints(endpoint_string)

            if valid_endpoint_string :
                environ['ENDPOINTS'] = valid_endpoint_string
                logger.info(f"ENDPOINTS : {environ['ENDPOINTS']}")
                dotenv.set_key(dotenv_file, "ENDPOINTS", environ["ENDPOINTS"])
                self.config.load_values()
                return json.loads(environ['ENDPOINTS'])

            else:
                return -1


        except Exception as error:
            raise error

    def get_valid_endpoints(self, endpoint_string):
        try:
            valid_endpoints   =  {'Endpoints' : [] }
            endpoint_json     =  json.loads(endpoint_string)
            endpoint_count    =  len(endpoint_json['Endpoints'])
            for idx in range(endpoint_count):

                server_url = "http://" + endpoint_json['Endpoints'][idx]['IP'] + ":" + \
                              endpoint_json['Endpoints'][idx]['Port']

                response = self.gw_sdk_healthcheck(server_url)
                if response:
                    if response.status_code == 200:
                        valid_endpoints['Endpoints'].append(endpoint_json['Endpoints'][idx])

            valid_endpoints_count = len(valid_endpoints['Endpoints'])

            if valid_endpoints_count == 0:
                return None

            return json.dumps(valid_endpoints)

        except Exception as e:
            raise ValueError(str(e))

    def gw_sdk_healthcheck(self, server_url):
        try:
            api_route = "api/health/"
            url=urljoin(server_url,api_route)

            response = requests.request("GET", url , verify=False, timeout=10)
            return response

        except Exception as e:
            logger.error(f'Configure_Env : gw_sdk_healthcheck : {e}')
            return None




