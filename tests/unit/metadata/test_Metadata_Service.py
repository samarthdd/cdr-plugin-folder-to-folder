import os
import sys
from unittest import TestCase
from metadata.Metadata_Service import Metadata_Service
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

class test_Metadata_Service(TestCase):

    def setUp(self) -> None:
        self.metadata_service = Metadata_Service()
        self.test_file = "./test_data/test_files/image1.jpg"

    def test_get_metadata(self):
        hd1_path="./test_path"
        content=self.metadata_service.get_metadata(self.test_file,hd1_path)
        assert content["original_file_paths"] is hd1_path

    def test_get_hash(self):
        hash=self.metadata_service.get_hash(self.test_file)
        assert hash is not None

