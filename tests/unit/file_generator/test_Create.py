import uuid
from unittest                                            import TestCase
from osbot_utils.utils.Files                             import file_exists,folder_delete_all,temp_folder

from cdr_plugin_folder_to_folder.file_generator.Create import Create
from os import path

class test_Create(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp_folder = temp_folder()

    @classmethod
    def tearDownClass(cls) -> None:
        folder_delete_all(cls.tmp_folder)

    def setUp(self) -> None:
        test_value          = uuid.uuid4()
        self.content   = str(test_value)
        self.file_name      = test_value.hex
        self.path = path.join(self.tmp_folder,self.file_name)

        self.file_creator = Create()

    def test_create(self):
        response=self.file_creator.create(self.path,"pdf",self.content)

        assert response      is None
        assert file_exists(self.path+".pdf")

    def test_create_failure(self):
        response = self.file_creator.create(self.path, "abc", self.content)
        assert response is not None
        assert file_exists(self.path) is False

    def test_create_pdf(self):
        response = self.file_creator.create(self.path, "pdf", self.content)
        assert response      is None
        filepath=self.path + ".pdf"
        assert file_exists(filepath)

    def test_create_docx(self):
        response = self.file_creator.create(self.path, "docx", self.content)
        assert response      is None
        assert file_exists(self.path + ".docx")

    def test_create_png(self):
        response = self.file_creator.create(self.path, "png", self.content)
        assert response      is None
        assert file_exists(self.path + ".png")

    def test_create_jpeg(self):
        response = self.file_creator.create(self.path, "jpeg", self.content)
        assert response      is None
        assert file_exists(self.path + ".jpeg")

    def test_create_jpg(self):
        response = self.file_creator.create(self.path, "jpg", self.content)
        assert response      is None
        assert file_exists(self.path + ".jpg")

    def test_create_gif(self):
        response = self.file_creator.create(self.path, "gif", self.content)
        assert response      is None
        assert file_exists(self.path + ".gif")

    def test_create_xlsx(self):
        response = self.file_creator.create(self.path, "xlsx", self.content)
        assert response      is None
        assert file_exists(self.path + ".xlsx")

    def test_create_txt(self):
        response = self.file_creator.create(self.path, "txt", self.content)
        assert response is None
        assert file_exists(self.path + ".txt")