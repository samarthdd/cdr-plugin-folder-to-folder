import uuid
from osbot_utils.utils.Files import file_create,create_folder
from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.file_generator.Create import Create
from os import path
import random

class File_Generator:

    def __init__(self, num_of_files, file_type, size=None):
        self.config = Config().load_values()

        self.num_of_files    = num_of_files
        self.file_type       = file_type
        self.size            = size

        self.target_folder   = path.join(self.config.file_generator_location, file_type)

        self.supported_types = [ "txt", "pdf", "docx", "xlsx", "jpg", "jpeg", "png", "gif" ]

    def populate(self):
        if self.file_type not in self.supported_types:
            return 0

        if self.num_of_files is 0:
            return -1

        create_folder(self.target_folder)
        for i in range(self.num_of_files):
            unique_value=uuid.uuid4()
            self.target_path = path.join(self.target_folder, unique_value.hex + "." + self.file_type)

            content = (str(unique_value) + "\n") * random.randint(1, 100000)

            file_creator = Create()
            file_creator.create(self.target_path, self.file_type, content)

        return 1






