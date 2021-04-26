from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Json import json_load_file

from cdr_plugin_folder_to_folder.processing.Analysis_Json import Analysis_Json
from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.utils.Elastic import Elastic
from cdr_plugin_folder_to_folder.utils.Logging import log_info


class Analysis_Elastic:

    def __init__(self):
        self.analysis_json = Analysis_Json()
        self.storage = Storage()
        self.config  = self.storage.config
        self.index_name = 'files_report_json'
        self.id_key = 'original_hash'
        self.enabled = False

    @cache_on_self
    def elastic(self):
        return Elastic(index_name=self.index_name, id_key=self.id_key)

    def setup(self, delete_existing=False):
        elastic = self.elastic()
        elastic.connect()
        elastic.setup()
        if elastic.enabled:
            elastic.create_index_and_index_pattern(delete_existing=delete_existing)
            self.enabled = True
        return self

    def all_analysis(self):
        return self.analysis_json.get_from_file()

    def add_analysis(self, report):
        return self.elastic().add(report)

    def delete_all_analysis(self):
        return self.setup(delete_existing=True)

    def load_analysis_from_report_file(self, hash):
        pass

    def reload_all_analysis(self):
        self.analysis_json.reset()
        metadatas = self.storage.hd2_metadatas(return_data=False)
        log_info(message=f"in reload_all_analysis there are {len(metadatas)}")
        for metadata in metadatas:
            file_hash = metadata.get_file_hash()
            file_name = metadata.get_file_name()
            report_json = json_load_file(metadata.report_file_path())
            if report_json:
                self.analysis_json.add_file(file_hash=file_hash, file_name=file_name)
                self.analysis_json.update_report(index=file_hash, report_json=report_json)
        self.analysis_json.write_to_file()
        message = f"in reload_all_analysis created analysis file with {len(self.analysis_json.analysis_data)} analysis"
        log_info(message)
        return message
