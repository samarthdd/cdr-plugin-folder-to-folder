from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from cdr_plugin_folder_to_folder.utils.Elastic import Elastic

class Events_Log_Elastic:
    def __init__(self):
        self.index_name = 'event_logs'
        self.id_key     = 'timestamp'
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

    def add_event_log(self, events_log):
        return self.elastic().add(events_log)

    def delete_event_log(self,timestamp):
        return self.elastic().delete(record_id=timestamp)

    def delete_all_event_logs(self):
        return self.setup(delete_existing=True)

    def get_all_event_logs(self):
        return self.elastic().search_using_lucene('*')

    def get_event_log(self, timestamp):
        return self.elastic().get_data(record_id=timestamp)
