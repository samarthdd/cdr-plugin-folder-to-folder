from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from cdr_plugin_folder_to_folder.utils.Elastic import Elastic

class Report_Elastic:
    def __init__(self):
        self.index_name = 'files_report_json'
        self.id_key     = 'original_hash'
        self.enabled    = False

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

    # class methods

    def add_report(self, report):
        return self.elastic().add(report)

    def delete_report(self,original_hash):
        return self.elastic().delete(record_id=original_hash)

    def delete_all_report(self):
        return self.setup(delete_existing=True)

    def get_all_report(self):
        return self.elastic().search_using_lucene('*')

    def get_report(self, original_hash):
        return self.elastic().get_data(record_id=original_hash)
