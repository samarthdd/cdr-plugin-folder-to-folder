from unittest import TestCase

import pytest
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set, random_text

from cdr_plugin_folder_to_folder.utils.Elastic import Elastic
from cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Index_Pattern import Index_Pattern
from cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana import Kibana


class test_Index_Pattern(TestCase):

    def setUp(self) -> None:
        if Elastic().server_online() is False:
            pytest.skip('Elastic server not available')
        self.pattern_name   = 'temp_index_pattern'
        self.kibana         = Kibana()
        self.index_pattern  = Index_Pattern(kibana=self.kibana, pattern_name=self.pattern_name)

    def test_create_info_exists_delete(self):
        result = self.index_pattern.create()
        pprint(result)
        assert result.get('attributes').get('title') == self.pattern_name
        assert self.index_pattern.exists() is True
        assert list_set(self.index_pattern.info()) == ['fields', 'id', 'namespaces', 'references', 'score', 'title',
                                                       'type', 'updated_at']
        assert Index_Pattern(kibana=self.kibana, pattern_name=random_text()).info() == {}
        assert self.index_pattern.delete() is True

    def test_create__time_field(self):
        time_field = random_text()
        self.index_pattern.create(time_field=time_field)
        assert self.index_pattern.info().get('timeFieldName') == time_field
        assert self.index_pattern.delete() is True

    def test_delete(self):
        assert self.index_pattern.delete() is False

    def test_id(self):
        assert self.index_pattern.id() is None

    def test_info(self):
        assert self.index_pattern.info() == {}