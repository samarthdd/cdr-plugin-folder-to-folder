from unittest import TestCase

import pytest
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import temp_file

from cdr_plugin_folder_to_folder.metadata.Metadata_Elastic import Metadata_Elastic
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing


class test_Metadata_Elastic(TestCase):

    def setUp(self) -> None:
        self.metadata_service = Metadata_Service()
        self.metadata_elastic = Metadata_Elastic()
        self.elastic          = self.metadata_elastic.elastic()
        Setup_Testing().set_config_for_local_testing(config=self.elastic.config)
        self.elastic.setup()
        if self.elastic.enabled is False:
            pytest.skip('Elastic server not available')

    def test_setup(self):
        self.metadata_elastic.setup()
        pprint(self.elastic.elastic().index_list())

    def test_add_metadata(self):
        file_path           = temp_file(contents='some text')
        metadata            = self.metadata_service.create_metadata(file_path=file_path, hd1_path=file_path)
        original_hash       = metadata.get('original_hash')
        result_add_metadata = self.metadata_elastic.add_metadata(metadata)

        assert original_hash == 'b94f6f125c79e3a5ffaa826f584c10d52ada669e6762051b826b55776d05aed2'
        assert result_add_metadata.get('_shards').get('successful') == 1

        assert self.metadata_elastic.get_metadata   (original_hash=original_hash)               == metadata
        assert self.metadata_elastic.delete_metadata(original_hash=original_hash).get('result') == 'deleted'
        assert self.metadata_elastic.get_metadata   (original_hash=original_hash)               == {}

    def test_clear_all_metadata(self):
        self.metadata_elastic.delete_all_metadata()
        assert len(self.metadata_elastic.get_all_metadata()) == 0



