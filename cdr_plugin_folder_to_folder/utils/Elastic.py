import osbot_elastic.elastic.ES
from osbot_elastic.Elastic_Search import Elastic_Search
from osbot_utils.decorators.methods.cache import cache

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.utils._to_refactor.For_Osbot_Elastic import For_Osbot_Elastic


class Elastic:

    def __init__(self, index='temp_index', time_field=None, id_key=None):
        self.config     = Config().load_values()
        self.id_key     = id_key
        self.index      = index
        self.time_field = time_field

    def connect(self):
        elastic_search = Elastic_Search(index='test_index')     # going to connect locally by default
        return elastic_search

    @cache
    def elastic(self) -> Elastic_Search:
        return self.connect()

    def add(self, data, refresh=False):
        return self.elastic().add(data, id_key=self.id_key, refresh=refresh)

    def setup(self, delete_existing=True):
        for_osbot_elastic = For_Osbot_Elastic(index=self.index, kibana=self.config.kibana_host,
                                              port=self.config.kibana_port)
        if delete_existing:
            self.elastic().api_index().delete_index()
            for_osbot_elastic.delete_index_pattern()
        #self.elastic().create_index()  # make sure index exists

        #for_osbot_elastic.create_index_pattern(time_field=self.time_field)  # make sure index pattern exists


#environ['ELASTIC_SERVER'] = self.config.elastic_host
#environ['ELASTIC_PORT'  ] = self.config.elastic_port
#environ['KIBANA_SERVER' ] = self.config.kibana_host
#environ['KIBANA_PORT'   ] = self.config.kibana_port