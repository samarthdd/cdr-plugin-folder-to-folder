from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import temp_folder, folder_files, folder_delete_all, folder_create, file_create_bytes, \
    file_contents_as_bytes, file_contents
from osbot_utils.utils.Misc import base64_to_str, base64_to_bytes, str_to_bytes, random_string, random_text

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.metadata.Metadata_Utils import Metadata_Utils
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from cdr_plugin_folder_to_folder.processing.Events_Log import Events_Log
from cdr_plugin_folder_to_folder.processing.File_Processing import File_Processing
from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.utils.file_utils import FileService
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data


class test_File_Processing(TestCase):

    config    = None
    temp_root = None
    #server = "34.245.221.234"

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_file = Test_Data().create_test_pdf(text=random_text(prefix="some random text: "))
        cls.config    = Config()
        cls.temp_root = folder_create('/tmp/temp_root') # temp_folder()
        cls.config.set_root_folder(root_folder=cls.temp_root)
        cls.metadata  = Metadata_Service().create_metadata(cls.test_file)


    @classmethod
    def tearDownClass(cls) -> None:
        #folder_delete_all(cls.config.root_folder)   # remove temp folder files
        cls.config.load_values()                    # reset config values

    def setUp(self) -> None:
        self.sdk_server      = '34.240.183.4'  # todo: use value from env variables
        self.sdk_port        = '8080'
        self.temp_folder     = temp_folder()
        self.events_log      = Events_Log(self.temp_folder)
        self.file_processing = File_Processing(events_log=self.events_log)
        self.storage         = Storage()

    def test_do_rebuild(self):
        pprint(self.metadata.metadata_folder_path())
        pprint(folder_files(self.config.root_folder,pattern="*"))
        endpoint    = f'http://{self.sdk_server}:{self.sdk_port}'
        hash        = Metadata_Utils().file_hash(self.test_file)
        encodedFile = FileService.base64encode(self.test_file)
        #dir         = './test_data/scenario-1/hd2/data/087a783915875b069c89d517491dd42b9e1b3619464a750e72a7ab44c06fa645'
        dir         = self.metadata.metadata_folder_path()
        self.file_processing.do_rebuild(endpoint=endpoint, hash=hash, encodedFile=encodedFile, dir=dir)

        pprint(self.events_log.get_from_file())

    def test_test_pdf(self,):

        pprint(file_contents(Test_Data().create_test_pdf()))