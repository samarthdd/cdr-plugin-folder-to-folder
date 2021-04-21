from unittest import TestCase
from unittest.mock import patch, call

import os
import json
import pytest

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import temp_file, file_delete, temp_folder, folder_delete_all, file_name, folder_copy
from osbot_utils.utils.Json import json_load_file

from cdr_plugin_folder_to_folder.processing.Report_Elastic import Report_Elastic
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
    )

class test_Report_Elastic(TestCase):
    test_file = None
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_file            = 'report.json'
        cls.file_hash            = '86df34018436a99e1e98ff51346591e189cd76c8518f7288bb1ea8336396259b'

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:

        report_file_path = os.path.join(FIXTURE_DIR, 'report.json')
        assert os.path.isfile(report_file_path)

        with open(report_file_path) as json_file:
            self.report_data = json.load(json_file) 

        self.original_hash   = self.report_data['original_hash']
        assert self.original_hash == self.file_hash

        self.report_elastic = Report_Elastic()

        if self.report_elastic.enabled is False:
            pytest.skip('Elastic server not available')

    def test_add_report(self):

        result_add_report = self.report_elastic.add_report(self.report_data)

        assert result_add_report.get('_shards').get('successful') == 1

        assert self.report_elastic.get_report   (original_hash=self.original_hash)               == report_data
        assert self.report_elastic.delete_report(original_hash=self.original_hash).get('result') == 'deleted'
        assert self.report_elastic.get_report   (original_hash=self.original_hash)               == {}

    def test_clear_all_report(self):
        self.report_elastic.delete_all_report()
        assert len(self.report_elastic.get_all_report()) == 0











