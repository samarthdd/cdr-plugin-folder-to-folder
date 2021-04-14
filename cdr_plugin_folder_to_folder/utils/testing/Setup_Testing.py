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

    def configure_config(self, config):
        self.set_config_for_local_testing(config=config)

    def configure_elastic(self, elastic):
        self.configure_config(config=elastic.config)

    def configure_metadata_elastic(self, metadata_elastic):
        self.configure_elastic(elastic=metadata_elastic.elastic())
        metadata_elastic.setup()

    def configure_pre_processor(self, pre_processor):
        metadata_elastic = pre_processor.meta_service.metadata_elastic
        self.configure_metadata_elastic(metadata_elastic=metadata_elastic)


