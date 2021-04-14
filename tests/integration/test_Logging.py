from unittest import TestCase

import pytest
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import random_text, list_set

from cdr_plugin_folder_to_folder.utils.Logging import Logging
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing


class test_Logging(TestCase):
    elastic = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.index_name = 'temp_log_index'
        cls.logging = Logging(index_name=cls.index_name)

        cls.elastic = cls.logging.elastic()
        Setup_Testing().configure_elastic(cls.elastic)
        cls.logging.setup()
        if cls.elastic.enabled is False:
            pytest.skip('Elastic server not available')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.elastic.index().delete_index()
        cls.elastic.index_pattern().delete()

    def setUp(self) -> None:
        self.logging.set_refresh_index(True)                # make messages sent to be index immediately

    def test_debug(self):
        record_id = self.logging.debug('an message').get('_id')
        assert self.elastic.get_data(record_id).get('level') == 'DEBUG'

    def test_info(self):
        message   = random_text()
        duration  = random_text()
        result    = self.logging.info(message, duration=duration)
        record_id = result.get('_id')
        assert result.get('_shards').get('successful') == 1

        data = self.elastic.get_data(record_id)
        assert data.get('level'   ) == 'INFO'
        assert data.get('message' ) == message
        assert data.get('duration') == duration

    def test_critical_debug_error_info_warning(self):
        message = random_text()
        self.logging.critical(message)
        self.logging.debug   (message)
        self.logging.error   (message)
        self.logging.info    (message)
        self.logging.warning (message)
        messages = self.elastic.search_using_lucene(message, index_by='level')

        assert list_set(messages) == ['CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'WARNING']
        assert messages['ERROR'].get('message') == message
