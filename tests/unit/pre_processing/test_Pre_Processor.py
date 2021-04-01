import os
import sys
from unittest import TestCase
from pre_processing.Pre_Processor import Pre_Processor
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from common_settings.config_params import Config
class test_Pre_Processor(TestCase):

    def setUp(self) -> None:
        self.pre_processor=Pre_Processor()

    def tearDown(self) -> None:
        pass

    def test_process_files(self):
        self.pre_processor.process_files()

        data_path=os.path.join(Config.hd2_location,"data")
        status_path=os.path.join(Config.hd2_location,"status")

        data_directory        =  os.listdir(data_path)
        status_directory      = os.listdir(status_path)

        assert len(data_directory) is not 0
        assert len(status_directory) is not 0

