from osbot_utils.decorators.methods.cache_on_self  import cache_on_self
from cdr_plugin_folder_to_folder.utils.Elastic     import Elastic

DEFAULT_TIME_FIELD = 'timestamp'

class Metadata_Elastic:
    def __init__(self):
        self.index_name = 'files_metadata'
        self.id_key     = 'original_hash'
        self.time_field = DEFAULT_TIME_FIELD
        self.enabled    = False

    @cache_on_self
    def elastic(self):
        return Elastic(index_name=self.index_name, id_key=self.id_key, time_field=self.time_field)

    def setup(self, delete_existing=False):
        elastic = self.elastic()
        elastic.connect()
        elastic.setup()
        if elastic.enabled:
            elastic.create_index_and_index_pattern(delete_existing=delete_existing)
            self.enabled = True
        return self

    # class methods

    def add_metadata(self, metadata):
        return self.elastic().add(metadata)

    def delete_metadata(self,original_hash):
        return self.elastic().delete(record_id=original_hash)

    def delete_all_metadata(self):
        return self.setup(delete_existing=True)

    def get_all_metadata(self):
        return self.elastic().search_using_lucene('*')

    def get_metadata(self, original_hash):
        return self.elastic().get_data(record_id=original_hash)

