from osbot_utils.utils.Files import path_combine, files_list


class Test_Data:

    def __init__(self):
        self.path_test_files = path_combine(__file__, '../../../../test_data/scenario-1/hd1')

    def files(self):
        return files_list(self.path_test_files)

    def json(self):
        return self.jsons().pop()

    def jsons(self):
        return files_list(self.path_test_files,"*.json")

    def image(self):
        return self.images().pop()

    def images(self):
        return files_list(self.path_test_files,"*.jpg")

    def pdfs(self):
        return files_list(self.path_test_files, "*.jpg")