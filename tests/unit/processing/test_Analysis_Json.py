from os.path import abspath
from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists, path_combine, temp_file, file_delete, file_name, file_not_exists
from osbot_utils.utils.Json import json_load_file
from osbot_utils.utils.Misc import list_set, random_string, str_sha256

from cdr_plugin_folder_to_folder.metadata.Metadata_Utils import Metadata_Utils
from cdr_plugin_folder_to_folder.processing.Analysis_Json import Analysis_Json
from cdr_plugin_folder_to_folder.metadata.Metadata import Metadata

import os
FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
    )

class test_Analysis_Json(TestCase):

    test_file = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_file      = temp_file(contents='Static text so that we have a static hash')
        cls.test_file_name = file_name(cls.test_file)
        cls.test_file_hash = '500286533bf75d769e9180a19414d1c3502dd52093e7351a0a9b1385d8f8961c'
        cls.meta_data={    'file_name'            : None               ,
                           'original_hash'       : '500286533bf75d769e9180a19414d1c3502dd52093e7351a0a9b1385d8f8961c'               ,
                           'rebuild_hash'         : None   }

    @classmethod
    def tearDownClass(cls) -> None:
        file_delete(cls.test_file)

    def setUp(self) -> None:
        self.analysis_json = Analysis_Json()
        self.storage   = self.analysis_json.storage
        report_file_path = os.path.join(FIXTURE_DIR, 'report.json')
        assert os.path.isfile(report_file_path)

        self.report_data = json_load_file(report_file_path)

    def test___init__(self):
        assert abspath(self.analysis_json.folder) == self.storage.hd2_status()

    @patch("multiprocessing.queues.Queue.put_nowait")
    def test_add_file(self, patch_put_nowait):
        analysis_data = self.analysis_json.get_from_file()
        if analysis_data.get('self.test_file_hash'):
            del analysis_data[self.test_file_hash]

        assert self.analysis_json.add_file(self.test_file_hash, self.test_file_name) is True
        assert analysis_data.get(self.test_file_hash) == {'file_name': self.test_file_name}

        assert self.analysis_json.add_file('AAAA'              , self.test_file_name) is False
        assert self.analysis_json.add_file(self.test_file_hash , None               ) is False
        assert self.analysis_json.add_file(None                , None               ) is False

        assert patch_put_nowait.mock_calls ==[call({'level': 'ERROR', 'message': 'in Analysis_Json.add_file bad data provided', 'data': {'file_hash': 'AAAA'                , 'file_name': self.test_file_name}, 'duration': 0, 'from_method': 'add_file', 'from_class': 'Analysis_Json'}),
                                              call({'level': 'ERROR', 'message': 'in Analysis_Json.add_file bad data provided', 'data': {'file_hash': self.test_file_hash   , 'file_name': None               }, 'duration': 0, 'from_method': 'add_file', 'from_class': 'Analysis_Json'}),
                                              call({'level': 'ERROR', 'message': 'in Analysis_Json.add_file bad data provided', 'data': {'file_hash': None                  , 'file_name': None               }, 'duration': 0, 'from_method': 'add_file', 'from_class': 'Analysis_Json'})]
        # assert patch_log_error.mock_calls == [call(message='in Analysis_Json.add_file bad data provided', data={'file_hash': 'AAAA'              , 'file_name': self.test_file_name }),
        #                                       call(message='in Analysis_Json.add_file bad data provided', data={'file_hash': self.test_file_hash , 'file_name': None                }),
        #                                       call(message='in Analysis_Json.add_file bad data provided', data={'file_hash': None                , 'file_name': None                })]


    def test_get_file_path(self):
        file_path = abspath(self.analysis_json.get_file_path())
        assert file_exists(file_path)
        assert file_path == path_combine(self.storage.hd2_status(), Analysis_Json.ANALYSIS_FILE_NAME)

    def test_get_from_file(self):
        data = self.analysis_json.get_from_file()
        assert type(data) is dict
        assert self.analysis_json.analysis_data == data

    def test_is_hash(self):
        test_file   = temp_file(contents='aaaa')
        file_hash   = Metadata_Utils().file_hash(test_file)                         # create hash from file
        text_hash   = str_sha256('asd')                                             # create hash from string

        assert self.analysis_json.is_hash(file_hash         ) is True                   # confirm both are valid hashes
        assert self.analysis_json.is_hash(text_hash         ) is True

        assert self.analysis_json.is_hash(None              ) is False                  # testing all sorts of conner cases
        assert self.analysis_json.is_hash(''                ) is False                  # empty strings
        assert self.analysis_json.is_hash('aaaa'            ) is False                  # non hash string
        assert self.analysis_json.is_hash(file_hash + 'aaaa') is False                  # confirm only exact matches work
        assert self.analysis_json.is_hash(text_hash + 'aaaa') is False
        assert self.analysis_json.is_hash('aaa' + file_hash ) is False
        assert self.analysis_json.is_hash(text_hash + '\nb`') is False                  # confirm content in new lines is also not a match
        assert self.analysis_json.is_hash('a\n' + file_hash ) is False

        file_delete(test_file)

    def test_write_to_file(self):
        target_file = temp_file()                                                   # temp file to save data
        assert file_not_exists(target_file)                                         # confirm it doesn't exist
        with patch.object(Analysis_Json, 'get_file_path', return_value=target_file):    # patch get_file_path to return temp file path
            assert self.analysis_json.get_file_path() == target_file                    # confirm patch is in place
            self.analysis_json.write_to_file()                                          # call write_to_file
            assert file_exists(target_file)                                         # confirm temp file now exists
            assert self.analysis_json.get_from_file() == self.analysis_json.analysis_data      # confirm reloaded data is correct
            assert json_load_file(target_file)    == self.analysis_json.analysis_data            # also confirm using direct json load of temp file
        assert self.analysis_json.get_file_path()     != target_file                    # confirm pathc is not there (after 'with' ends)
        file_delete(target_file)                                                    # delete temp file

    def test_update_report(self):
        temp_data_file = temp_file()
        with patch.object(Analysis_Json, 'get_file_path', return_value=temp_data_file):
            self.analysis_json.add_file(self.test_file_hash, self.test_file_name)
            self.analysis_json.update_report(self.test_file_hash, self.report_data)
        pprint(self.analysis_json.get_from_file())

    def test_get_file_analysis(self):
        with patch.object(Metadata, 'get_from_file', return_value=self.meta_data):
            response=self.analysis_json.get_file_analysis(self.test_file_hash, self.report_data)
            pprint(response)
            assert "file_name" in response
            assert "original_hash"         in response
            assert response["original_hash"]    == self.test_file_hash
            assert "rebuild_hash"          in response
            assert "file_type"             in response
            assert "file_size"             in response
            assert "remediated_item_count" in response
            assert "remediate_items_list"  in response
            assert "sanitised_item_count"  in response
            assert "sanitised_items_list"  in response
            assert "issue_item_count"      in response
            assert "issue_item_list"       in response

    def test_get_remediated_item_details(self):
        count,list = self.analysis_json.get_remediated_item_details(self.report_data)
        assert count is not None
        assert list  is not None
        assert count == len(list)

    def test_get_sanitisation_item(self):
        count,list = self.analysis_json.get_sanitisation_item_details(self.report_data)
        assert count is not None
        assert list  is not None
        assert count == len(list)

    def test_get_issue_item_details(self):
        count,list = self.analysis_json.get_issue_item_details(self.report_data)
        assert count is not None
        assert list  is not None
        assert count == len(list)








