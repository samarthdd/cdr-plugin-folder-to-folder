from unittest import TestCase
from unittest.mock import patch, call

import os
import pytest

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import json_load_file

from cdr_plugin_folder_to_folder.processing.Events_Log_Elastic import Events_Log_Elastic
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
    )

class test_Events_Log_Elastic(TestCase):
    test_file = None
    @classmethod
    def setUpClass(cls) -> None:
        cls.file_hash            = '86df34018436a99e1e98ff51346591e189cd76c8518f7288bb1ea8336396259b'

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:

        events_file_path = os.path.join(FIXTURE_DIR, 'events.json')
        assert os.path.isfile(events_file_path)

        self.events_data = json_load_file(events_file_path)

        self.events_log_elastic = Events_Log_Elastic()
        self.events_log_elastic.setup()

        if self.events_log_elastic.enabled is False:
            pytest.skip('Elastic server not available')

    def test_add_events(self):

        assert len(self.events_data["events"]) > 0

        for event_log in self.events_data["events"]:
            result_add_event = self.events_log_elastic.add_event_log(event_log)
            assert result_add_event.get('_shards').get('successful') == 1

        first_event = self.events_data["events"][0]
        first_timestamp = first_event["timestamp"]

        assert self.events_log_elastic.get_event_log (timestamp=first_timestamp)               == first_event
        assert self.events_log_elastic.delete_event_log  (timestamp=first_timestamp).get('result') == 'deleted'
        assert self.events_log_elastic.get_event_log (timestamp=first_timestamp)               == {}

    def test_clear_all_events(self):
        self.events_log_elastic.delete_all_event_logs()
        assert len(self.events_log_elastic.get_all_event_logs()) == 0











