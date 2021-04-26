from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists
from osbot_utils.utils.Json import json_load_file

from cdr_plugin_folder_to_folder.processing.Analysis_Elastic import Analysis_Elastic
from cdr_plugin_folder_to_folder.utils.testing.Temp_Config import Temp_Config


class test_Analysis_Elastic(Temp_Config):

    def setUp(self) -> None:
        self.analysis_elastic = Analysis_Elastic()
        self.storage          = self.analysis_elastic.storage
        self.config           = self.storage.config
        self.config.set_root_folder('/Users/diniscruz/_dev/filetrust/cdr-plugin-folder-to-folder/test_data/scenario-2')

    def test_load_analysis_from_report_file(self):
        self.analysis_elastic.reload_all_analysis()





