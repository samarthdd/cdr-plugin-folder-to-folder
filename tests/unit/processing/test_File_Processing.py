from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import temp_folder, folder_files, folder_delete_all, folder_create, file_create_bytes, \
    file_contents_as_bytes, file_contents, file_name
from osbot_utils.utils.Http import POST, POST_json
from osbot_utils.utils.Json import json_to_str
from osbot_utils.utils.Misc import base64_to_str, base64_to_bytes, str_to_bytes, random_string, random_text, \
    str_to_base64, bytes_to_str, bytes_to_base64

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.metadata.Metadata_Utils import Metadata_Utils
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from cdr_plugin_folder_to_folder.processing.Events_Log import Events_Log
from cdr_plugin_folder_to_folder.processing.File_Processing import File_Processing
from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.utils.file_utils import FileService
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data
from cdr_plugin_folder_to_folder.processing.Report_Elastic import Report_Elastic
from cdr_plugin_folder_to_folder.processing.Analysis_Json import Analysis_Json

class test_File_Processing(TestCase):

    config    = None
    temp_root = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_file = Test_Data().create_test_pdf(text=random_text(prefix="some random text: "))
        cls.test_file_name = file_name(cls.test_file)
        cls.config    = Config()
        cls.temp_root = folder_create('/tmp/temp_root') # temp_folder()
        cls.config.set_root_folder(root_folder=cls.temp_root)
        cls.meta_service = Metadata_Service()
        cls.metadata  = cls.meta_service.create_metadata(cls.test_file)
        cls.analysis_json = Analysis_Json()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.config.load_values()                    # reset config values

    def setUp(self) -> None:
        self.sdk_server      = '91.109.25.88'  # todo: use value from env variables
        self.sdk_port        = '8080'
        self.temp_folder     = temp_folder()
        self.events_log      = Events_Log(self.temp_folder)
        self.report_elastic  = Report_Elastic()
        self.file_processing = File_Processing(events_log=self.events_log, report_elastic=self.report_elastic, meta_service=self.meta_service )
        self.storage         = Storage()

    def test_do_rebuild(self):
        pprint(self.metadata.metadata_folder_path())
        pprint(folder_files(self.config.root_folder,pattern="*"))
        endpoint    = f'http://{self.sdk_server}:{self.sdk_port}'
        hash        = Metadata_Utils().file_hash(self.test_file)
        assert self.analysis_json.add_file(hash, self.test_file_name) is True
        dir         = self.metadata.metadata_folder_path()
        self.file_processing.do_rebuild(endpoint=endpoint, hash=hash, source_path=self.test_file, dir=dir)

        pprint(self.events_log.get_from_file())

    # target_file     = '/tmp/rebuilt-file.pdf'

    def test_pdf_rebuild(self,):
        #server         = "84.16.229.232"  # aws                                            # 5.1 lowest response time
        server          = "192.168.0.249"   # local                                         # 3.9 lowest response time
        server          = "cdr-plugin-dev-sdk-lb-1930604683.eu-west-1.elb.amazonaws.com"    # 4.5 lowest response time
        url             = f"http://{server}:8080/api/rebuild/base64"
        headers         = { 'accept': 'application/json',
                            'Content-Type': 'application/json'}
        text            = random_text("random text - ")
        test_pdf        = Test_Data().create_test_pdf(text=text)
        original_bytes  = file_contents_as_bytes(test_pdf)

        original_base64 = bytes_to_base64(original_bytes)
        post_data       = {"Base64": original_base64}
        result          = POST(url, data=post_data, headers=headers)
        rebuild_base64 = base64_to_bytes(result)

        assert str_to_bytes(text)     in     original_bytes
        assert b'Glasswall Processed' not in original_bytes

        assert str_to_bytes(text)     in     rebuild_base64
        assert b'Glasswall Processed' in     rebuild_base64
