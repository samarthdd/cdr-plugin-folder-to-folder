from unittest import TestCase
from osbot_utils.utils.Files import folder_exists, path_combine
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing


class test_Setup_Testing(TestCase):
    def setUp(self) -> None:
        self.setup_testing = Setup_Testing()

    def test_path_repo_root(self):
        path_repo = self.setup_testing.path_repo_root()
        assert folder_exists(path_repo)
        assert folder_exists(path_combine(path_repo, '.git'))
        assert folder_exists(path_combine(path_repo, 'test_data'))

    def test_set_test_root_dir(self):
        self.setup_testing.set_test_root_dir()
        assert folder_exists(path_combine('.', '.git'))
        assert folder_exists(path_combine('.', 'test_data'))