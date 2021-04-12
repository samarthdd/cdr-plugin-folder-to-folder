import osbot_elastic.elastic.ES
from osbot_elastic.Elastic_Search import Elastic_Search
from osbot_elastic.elastic.Index import Index
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache import cache
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Http import GET_json

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Index_Pattern import Index_Pattern
from cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana import Kibana


class Elastic:

    def __init__(self, index_name='temp_index', time_field=None, id_key=None):
        self.config             = Config().load_values()
        self.id_key             = id_key
        self.index_name         = index_name
        self.index_pattern_name = index_name
        self.time_field         = time_field

    def connect(self):
        elastic_search = Elastic_Search(index=self.index_name)     # going to connect locally by default
        return elastic_search

    def server_online(self):
        server_url = f'{self.config.elastic_schema}://{self.config.elastic_host}:{self.config.elastic_port}'
        try:
            return GET_json(server_url).get('tagline') == 'You Know, for Search'
        except:
            return False

    # cached objects
    @cache_on_self
    def index(self) -> Index:
        return self.elastic().api_index()

    @cache_on_self
    def index_pattern(self):
        return Index_Pattern(kibana=self.kibana(), pattern_name=self.index_pattern_name)

    @cache_on_self
    def elastic(self) -> Elastic_Search:
        return self.connect()

    @cache_on_self
    def kibana(self) -> Kibana:
        kibana_host = self.config.kibana_host
        kibana_port = self.config.kibana_port
        return Kibana(index_name=self.index_name, host=kibana_host, port=kibana_port)

    # class methods

    def add(self, data, refresh=False):
        return self.elastic().add(data, id_key=self.id_key, refresh=refresh)

    def get_data(self, record_id):
        result = self.elastic().get_data(id=record_id)
        if result:
            return result.get('_source')
        return {}

    @index_by
    @group_by
    def search_using_lucene(self, query='*', size=10000):
        return list(self.elastic().search_using_lucene(query, size=size))

    def setup(self, delete_existing=False):
        if delete_existing:
            self.index().delete_index()
            self.index_pattern().delete()

        self.index().create()
        self.index_pattern().create(time_field=self.time_field)
        return self


#environ['ELASTIC_SERVER'] = self.config.elastic_host
#environ['ELASTIC_PORT'  ] = self.config.elastic_port
#environ['KIBANA_SERVER' ] = self.config.kibana_host
#environ['KIBANA_PORT'   ] = self.config.kibana_port