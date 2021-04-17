from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set

from cdr_plugin_folder_to_folder.pre_processing.Hash_Json import Hash_Json


class test_Hash_Json(TestCase):

    def setUp(self) -> None:
        self.hash_json = Hash_Json()

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
