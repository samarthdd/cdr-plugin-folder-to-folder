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

    def test_create_metadata(self):

        metadata  = self.metadata_service.create_metadata(self.test_file)
        metadata.delete()
        metadata.add_file(self.test_file)

        assert metadata.data == {  'file_name'           : file_name(self.test_file)  ,
                                   'original_file_paths' : [self.test_file]           ,
                                   'original_hash'       : file_sha256(self.test_file),
                                   'rebuild_hash'        : None                       ,
                                   'rebuild_status'      : FileStatus.INITIAL.value   ,
                                   'target_path'         : None                       ,
                                   'xml_report_status'   : None                       ,
                                   'error'               : None                       ,
                                 }
        assert metadata.delete() is True

    def test_file_hash(self):
        hash=self.metadata_service.file_hash(self.test_file)
        assert hash == file_sha256(self.test_file)

    def test_file_hash_metadata(self):
        pass

