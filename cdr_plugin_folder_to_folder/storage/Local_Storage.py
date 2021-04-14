from osbot_utils.utils.Files import temp_folder

from cdr_plugin_folder_to_folder.common_settings.Config import Config


class Local_Storage:
    def __init__(self):
        self.config    = Config()
        self.path_hd1  = None
        self.path_hd2  = None
        self.path_hd3  = None
        self.path_root = None

    def hd1(self):
        return self.config.hd1_location

    def hd2(self):
        return self.config.hd2_location

    def hd3(self):
        return self.config.hd3_location





