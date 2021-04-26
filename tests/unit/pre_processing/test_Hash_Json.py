from os.path import abspath
from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists, path_combine, temp_file, file_delete, file_name, file_not_exists
from osbot_utils.utils.Json import json_load_file
from osbot_utils.utils.Misc import list_set, random_string, str_sha256

from cdr_plugin_folder_to_folder.metadata.Metadata_Utils import Metadata_Utils
from cdr_plugin_folder_to_folder.pre_processing.Hash_Json import Hash_Json


class test_Hash_Json(TestCase):

    test_file = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_file      = temp_file(contents='Static text so that we have a static hash')
        cls.test_file_name = file_name(cls.test_file)
        cls.test_file_hash = '500286533bf75d769e9180a19414d1c3502dd52093e7351a0a9b1385d8f8961c'

    @classmethod
    def tearDownClass(cls) -> None:
        file_delete(cls.test_file)

    def setUp(self) -> None:
        self.hash_json = Hash_Json()
        self.storage   = self.hash_json.storage

    def test___init__(self):
        assert abspath(self.hash_json.folder) == self.storage.hd2_status()

    @patch("multiprocessing.queues.Queue.put_nowait")
    def test_add_file(self, patch_log_error):
        hash_data = self.hash_json.get_from_file()
        if hash_data.get('self.test_file_hash'):
            del hash_data[self.test_file_hash]

        assert self.hash_json.add_file(self.test_file_hash, self.test_file_name) is True
        assert hash_data.get(self.test_file_hash) == {'file_name': self.test_file_name, 'file_status': 'Initial'}

        assert self.hash_json.add_file('AAAA'              , self.test_file_name) is False
        assert self.hash_json.add_file(self.test_file_hash , None               ) is False
        assert self.hash_json.add_file(None                , None               ) is False

        assert patch_log_error.mock_calls == [call({'level': 'ERROR', 'message': 'in Hash_Json.add_file bad data provided', 'data': {'file_hash': 'AAAA'             , 'file_name': self.test_file_name}, 'duration': 0, 'from_method': 'add_file', 'from_class': 'Hash_Json'}),
                                              call({'level': 'ERROR', 'message': 'in Hash_Json.add_file bad data provided', 'data': {'file_hash': self.test_file_hash, 'file_name': None               }, 'duration': 0, 'from_method': 'add_file', 'from_class': 'Hash_Json'}),
                                              call({'level': 'ERROR', 'message': 'in Hash_Json.add_file bad data provided', 'data': {'file_hash': None               , 'file_name': None               }, 'duration': 0, 'from_method': 'add_file', 'from_class': 'Hash_Json'})]



    def test_get_file_path(self):
        file_path = abspath(self.hash_json.get_file_path())
        assert file_exists(file_path)
        assert file_path == path_combine(self.storage.hd2_status(), Hash_Json.HASH_FILE_NAME)

    def test_get_from_file(self):
        data = self.hash_json.get_from_file()
        assert type(data) is dict
        assert self.hash_json.data == data

    def test_get_json_list(self):
        assert self.hash_json.get_json_list() == self.hash_json.data

    def test_is_hash(self):
        test_file   = temp_file(contents='aaaa')
        file_hash   = Metadata_Utils().file_hash(test_file)                         # create hash from file
        text_hash   = str_sha256('asd')                                             # create hash from string

        assert self.hash_json.is_hash(file_hash         ) is True                   # confirm both are valid hashes
        assert self.hash_json.is_hash(text_hash         ) is True

        assert self.hash_json.is_hash(None              ) is False                  # testing all sorts of conner cases
        assert self.hash_json.is_hash(''                ) is False                  # empty strings
        assert self.hash_json.is_hash('aaaa'            ) is False                  # non hash string
        assert self.hash_json.is_hash(file_hash + 'aaaa') is False                  # confirm only exact matches work
        assert self.hash_json.is_hash(text_hash + 'aaaa') is False
        assert self.hash_json.is_hash('aaa' + file_hash ) is False
        assert self.hash_json.is_hash(text_hash + '\nb`') is False                  # confirm content in new lines is also not a match
        assert self.hash_json.is_hash('a\n' + file_hash ) is False

        file_delete(test_file)

    def test_write_to_file(self):
        target_file = temp_file()                                                   # temp file to save data
        assert file_not_exists(target_file)                                         # confirm it doesn't exist
        with patch.object(Hash_Json, 'get_file_path', return_value=target_file):    # patch get_file_path to return temp file path
            assert self.hash_json.get_file_path() == target_file                    # confirm patch is in place
            self.hash_json.write_to_file()                                          # call write_to_file
            assert file_exists(target_file)                                         # confirm temp file now exists
            assert self.hash_json.get_from_file() == self.hash_json.data            # confirm reloaded data is correct
            assert json_load_file(target_file)    == self.hash_json.data            # also confirm using direct json load of temp file
        assert self.hash_json.get_file_path()     != target_file                    # confirm pathc is not there (after 'with' ends)
        file_delete(target_file)                                                    # delete temp file

    def test_update_status(self):
        temp_data_file = temp_file()
        with patch.object(Hash_Json, 'get_file_path', return_value=temp_data_file):
            self.hash_json.add_file(self.test_file_hash, self.test_file_name)
            assert self.hash_json.data[self.test_file_hash]['file_status'] == 'Initial'
            self.hash_json.update_status(self.test_file_hash, 'BBBB')
            assert self.hash_json.data[self.test_file_hash]['file_status'] == 'BBBB'
            assert json_load_file(temp_data_file)[self.test_file_hash]['file_status'] == 'BBBB'
        pprint(self.hash_json.get_from_file())

    def test_get_json_list__bug(self):                                  # this test confirms the bug
        hashes = self.hash_json.get_json_list()
        for hash in self.hash_json.get_json_list():
            if len(hash) == 64:                                         # all keys in this object should be a hash
                assert len(hash) == 64
                assert type(hashes[hash]) == dict                       # with all items being a dictionary
                assert list_set(hashes[hash]) == ['file_name', 'file_status']
            else:
                assert hash == "file_list"                              # but the old schema is still present
                assert type(hashes[hash]) == list                       # with the data being a list
                assert list_set(hashes[hash][0]) == ['file_name', 'file_status', 'hash', 'id']



