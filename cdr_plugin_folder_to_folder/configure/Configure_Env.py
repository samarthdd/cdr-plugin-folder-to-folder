import os
from cdr_plugin_folder_to_folder.common_settings.Config import Config

import logging as logger
from os import environ
logger.basicConfig(level=logger.INFO)

class Configure_Env:
    def __init__(self):
        pass

    # def hard_discs_details(self):
    #     try:
    #
    #         return {
    #             "hd1_path": environ.get('HD1_LOCATION'),
    #             "hd2_path": environ.get('HD2_LOCATION'),
    #             "hd3_path": environ.get('HD3_LOCATION')
    #         }
    #     except Exception as error:
    #         raise error
    #
    # def configure_hard_discs(self, hd1_path=None, hd2_path=None, hd3_path=None):
    #     try:
    #         environ["MODE"]="1"
    #         if hd1_path:
    #             if os.path.exists(hd1_path):
    #                 environ['HD1_LOCATION'] = hd1_path
    #             else:
    #                 return 0
    #         if hd2_path:
    #             if os.path.exists(hd1_path):
    #                 environ['HD2_LOCATION'] = hd2_path
    #             else:
    #                 return 0
    #
    #         if hd3_path:
    #             if os.path.exists(hd1_path):
    #                 environ['HD3_LOCATION'] = hd3_path
    #             else:
    #                 return 0
    #         return self.hard_discs_details()
    #
    #     except Exception as error:
    #         raise ValueError(str(error))
    #
    # def gw_sdk_details(self):
    #     try:
    #
    #         return {
    #             "gw_address": environ.get('GW_SDK_ADDRESS'),
    #             "gw_port": environ.get('GW_SDK_PORT'),
    #         }
    #     except Exception as error:
    #         raise error
    #
    #
    #
    # def configure_gw_sdk_endpoints(self, gw_address=None, gw_port=None):
    #     try:
    #         environ["MODE"]="1"
    #         if gw_address:
    #             environ['GW_SDK_ADDRESS'] = gw_address
    #         if gw_port:
    #             if int(gw_port):
    #                 environ['GW_SDK_PORT'] = gw_port
    #         return self.gw_sdk_details()
    #
    #     except Exception as e:
    #         raise ValueError(str(e))

    def configure(self, hd1_path=None, hd2_path=None, hd3_path=None,gw_address=None, gw_port=None):
        try:
            if hd1_path:
                if os.path.exists(hd1_path):
                    environ['HD1_LOCATION'] = hd1_path
                else:
                    return 0
            if hd2_path:
                if os.path.exists(hd1_path):
                    environ['HD2_LOCATION'] = hd2_path
                else:
                    return 0
            if hd3_path:
                if os.path.exists(hd1_path):
                    environ['HD3_LOCATION'] = hd3_path
                else:
                    return 0
            if gw_address:
                environ['GW_SDK_ADDRESS'] = gw_address
            if gw_port:
                if int(gw_port):
                    environ['GW_SDK_PORT'] = gw_port
                else:
                    return 0
            environ["MODE"]="1"

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

    def reset_mode(self):
        try:
            if "MODE" in environ:
                del environ["MODE"]
            return "Reset Completed"
        except Exception as e:
            raise e





