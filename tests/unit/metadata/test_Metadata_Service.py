from unittest                                            import TestCase
from osbot_utils.utils.Files                             import file_exists, file_sha256, file_name
from cdr_plugin_folder_to_folder.utils.testing.Test_Data import Test_Data
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.pre_processing.Status import FileStatus

class test_Metadata_Service(TestCase):

    def setUp(self) -> None:
        self.metadata_service = Metadata_Service()
        self.test_file        = Test_Data().images().pop()
        assert file_exists(self.test_file)

    def test_get_metadata(self):
        hd1_path= "./test_path"
        metadata  =self.metadata_service.get_metadata(self.test_file,hd1_path)

        assert metadata == {  'evidence_file_paths' : None                       ,
                              'file_name'           : file_name(self.test_file)  ,
                              'original_file_paths' : hd1_path                   ,
                              'original_hash'       : file_sha256(self.test_file),
                              'rebuild_status'      : FileStatus.INITIAL.value   ,
                              'target_path'         : None                       ,
                              'xml_report_status'   : None                       ,
                              'error'               : None                       ,
                              }

    def test_get_hash(self):
        hash=self.metadata_service.get_hash(self.test_file)
        assert hash == file_sha256(self.test_file)

