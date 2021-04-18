from os.path import abspath

from osbot_utils.utils.Files import temp_folder, path_combine

from cdr_plugin_folder_to_folder.common_settings.Config import Config


class Storage:
    def __init__(self):
        self.config    = Config()
        self.path_hd1  = None
        self.path_hd2  = None
        self.path_hd3  = None
        self.path_root = None

    def hd1(self, path=''):
        return path_combine(self.config.hd1_location, path)

    def hd2(self):
        return abspath(self.config.hd2_location                   )   # convert to absolute paths

    def hd2_data(self, path=''):
        return path_combine(self.config.hd2_data_location, path   )   # add path and convert to absolute paths

    def hd2_status(self, path=''):
        return path_combine(self.config.hd2_status_location, path )  # add path and convert to absolute paths

    def hd3(self, path=''):
        return path_combine(self.config.hd3_location, path        )  # add path and convert to absolute paths





