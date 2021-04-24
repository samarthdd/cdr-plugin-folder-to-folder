import cdr_plugin_folder_to_folder
from os import chdir, environ
from osbot_utils.utils.Files import parent_folder, temp_folder, folder_delete_all


class Setup_Testing:

    def __init__(self, configure_logging=True):
        self.temp_root_folder = None
        if configure_logging:
            self.configure_static_logging()                                     # todo refactor once this logging use of static object is also refactored

    def path_repo_root(self):
        """find the root path via getting the parent folder of the location of the
           cdr_plugin_folder_to_folder module"""
        return parent_folder(cdr_plugin_folder_to_folder.__path__[0])

    def set_test_root_dir(self):                                                # todo refactor this since it is causing a circular reference with Config (i.e. preventing Config from being used here)
        """make sure the current test execution directory is the root of the repo"""
        path_repo = self.path_repo_root()
        chdir(path_repo)
        return path_repo

    def configure_config(self, config):
        config.kibana_host = '127.0.0.1'
        config.elastic_host = '127.0.0.1'
        return self

    def configure_elastic(self, elastic):
        self.configure_config(config=elastic.config)
        elastic.setup()
        return self

    def configure_logging(self, logging):
        self.configure_config(logging.elastic().config)
        logging.setup()
        return self

    def configure_metadata_elastic(self, metadata_elastic):
        self.configure_elastic(elastic=metadata_elastic.elastic())
        metadata_elastic.setup()
        return self

    def configure_pre_processor(self, pre_processor):
        metadata_elastic = pre_processor.meta_service.metadata_elastic
        self.configure_metadata_elastic(metadata_elastic=metadata_elastic)
        return self


    def configure_static_logging(self):
        from cdr_plugin_folder_to_folder.utils.Logging import logging
        self.configure_logging(logging=logging)
        return self

    def get_config(self):
        from cdr_plugin_folder_to_folder.common_settings.Config import Config       # needs to be here due to circular references with this class and Config
        return Config()

    def set_config_to_temp_folder(self):
        self.temp_root_folder = temp_folder()
        self.get_config().set_root_folder(root_folder=self.temp_root_folder)

    def restore_config(self):
        folder_delete_all(self.temp_root_folder)
        self.get_config().load_values()                               # reload config values