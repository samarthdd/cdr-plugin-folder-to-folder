import os
import shutil
from unittest import TestCase

from pre_processing.utils.File_Service import File_Service
class test_File_service(TestCase):
    test_folder="./test_data/test_files"
    new_folder=os.path.join(test_folder, "sample")

    def setUp(self) -> None:
        self.file_service=File_Service()
        self.test_folder=test_File_service.test_folder
        self.test_file =  os.path.join(self.test_folder,"image1.jpg")
        self.new_folder = test_File_service.new_folder
        self.dict_content={}
        self.dict_content["value"]="testing"

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(test_File_service.new_folder)
        pass

    def test_copy_file(self):
        self.dst = os.path.join(self.test_folder,"image2.jpg")
        self.file_service.copy_file(self.test_file,self.dst )

        assert os.path.exists(self.dst) is True

    def test_create_folder(self):
        self.file_service.create_folder(self.new_folder)

        assert os.path.exists(self.new_folder) is True

    def test_copy_folder(self):
        self.file_service.copy_folder(self.test_folder,self.new_folder)
        directory = os.listdir(self.new_folder)

        assert len(directory) is not 0


    def test_wrtie_json_file(self):
        self.file_service.create_folder(self.new_folder)
        self.file_service.wrtie_json_file(self.new_folder,"test.json",self.dict_content)

        assert os.path.exists(os.path.join(self.new_folder,"test.json")) is True

    def test_read_json_file(self):
        json_file_path=os.path.join(self.test_folder,"test.json")
        content=self.file_service.read_json_file(json_file_path)

        assert content is not None

    def test_move_file(self):
        if not os.path.exists(self.new_folder):
            os.makedirs(self.new_folder)
        self.src = os.path.join(self.test_folder, "image2.jpg")
        self.file_service.move_file(self.src, os.path.join(self.new_folder,"image1.jpg"))

        assert os.path.exists(self.src ) is False


    def test_delete_folder(self):
        self.file_service.delete_folder(self.new_folder)

        assert os.path.exists(self.new_folder) is False



