import cdr_plugin_folder_to_folder
from os import chdir, environ
from   osbot_utils.utils.Files      import parent_folder


class Setup_Testing:

    def path_repo_root(self):
        """find the root path via getting the parent folder of the location of the
           cdr_plugin_folder_to_folder module"""
        return parent_folder(cdr_plugin_folder_to_folder.__path__[0])

    def set_test_root_dir(self):
        """make sure the current test execution directory is the root of the repo"""
        path_repo = self.path_repo_root()
        chdir(path_repo)
        return path_repo

    def set_config_for_local_testing(self, config=None):
        from cdr_plugin_folder_to_folder.utils.Logging import logging
        if config is None:
            config = logging.elastic().config
        config.kibana_host  = '127.0.0.1'
        config.elastic_host = '127.0.0.1'
        logging.setup()