import osbot_elastic.elastic.ES
from osbot_elastic.Elastic_Search import Elastic_Search
from osbot_elastic.elastic.Index import Index
from osbot_utils.decorators.methods.cache import cache
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
    @cache
    def index(self) -> Index:
        return self.elastic().api_index()

    @cache
    def index_pattern(self):
        return Index_Pattern(kibana=self.kibana(), pattern_name=self.index_pattern_name)

    @cache
    def elastic(self) -> Elastic_Search:
        return self.connect()

    @cache
    def kibana(self) -> Kibana:
        kibana_host = self.config.kibana_host
        kibana_port = self.config.kibana_port
        return Kibana(index_name=self.index_name, host=kibana_host, port=kibana_port)

    # class methods

    def add(self, data, refresh=False):
        return self.elastic().add(data, id_key=self.id_key, refresh=refresh)

    def setup(self, delete_existing=True):
        if delete_existing:
            self.index().delete_index()
            self.index_pattern().delete()

        self.index().create()
        self.index_pattern().create(time_field=self.time_field)
        #self.elastic().create_index()  # make sure index exists

        #for_osbot_elastic.create_index_pattern(time_field=self.time_field)  # make sure index pattern exists


#environ['ELASTIC_SERVER'] = self.config.elastic_host
#environ['ELASTIC_PORT'  ] = self.config.elastic_port
#environ['KIBANA_SERVER' ] = self.config.kibana_host
#environ['KIBANA_PORT'   ] = self.config.kibana_port