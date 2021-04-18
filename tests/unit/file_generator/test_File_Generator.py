from unittest                                            import TestCase
from osbot_utils.utils.Files                             import temp_folder,folder_delete_all

from cdr_plugin_folder_to_folder.file_generator.File_Generator import File_Generator

class test_File_Generator(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp_folder = temp_folder()

    @classmethod
    def tearDownClass(cls) -> None:
        folder_delete_all(cls.tmp_folder)

    def setUp(self) -> None:
        self.num_of_files=4
        self.file_type="pdf"

    def test_populate(self):
        self.file_generator = File_Generator(self.num_of_files, self.file_type)
        response= self.file_generator.populate()
        assert response is 1

    def test_populate_failure_1(self):
        self.file_generator = File_Generator(self.num_of_files, "abc")
        response = self.file_generator.populate()
        assert response is 0

    def test_populate_failure_2(self):
        self.file_generator = File_Generator(0, "pdf")
        response = self.file_generator.populate()
        assert response is -1



