from unittest                                            import TestCase
from osbot_utils.utils.Files                             import folder_delete_all, folder_copy

import shutil
from cdr_plugin_folder_to_folder.file_generator.File_Generator import File_Generator
from cdr_plugin_folder_to_folder.common_settings.Config import Config
from os import path, listdir

class test_File_Generator(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp_folder = "../temp_generator_folder"

        cls.config=Config().load_values()

        folder_delete_all(cls.tmp_folder)
        folder_copy(cls.config.file_generator_location, cls.tmp_folder)
        folder_delete_all(cls.config.file_generator_location)

    @classmethod
    def tearDownClass(cls) -> None:
        folder_delete_all(cls.config.file_generator_location)
        folder_copy(cls.tmp_folder, cls.config.file_generator_location)
        folder_delete_all(cls.tmp_folder)

    def setUp(self) -> None:
        self.num_of_files=4
        self.file_type="pdf"

    def test_populate(self):
        self.file_generator = File_Generator(self.num_of_files, self.file_type)

        target_folder = path.join(self.config.file_generator_location, "pdf")
        response= self.file_generator.populate()

        # check response is 1
        assert response is 1

        # check number of files is equal to 5 be 4
        num_of_existing_files = len(
            [name for name in listdir(target_folder) if path.isfile(path.join(target_folder, name))])
        assert num_of_existing_files is 4

    def test_populate_failure_1(self):
        self.file_generator = File_Generator(self.num_of_files, "abc")
        response = self.file_generator.populate()

        # check response is 0 since 'abc' is not valid file type
        assert response is 0

    def test_populate_failure_2(self):
        self.file_generator = File_Generator(0, "pdf")
        response = self.file_generator.populate()

        # check response is -1 since 0 is not valid num_of_files
        assert response is -1



