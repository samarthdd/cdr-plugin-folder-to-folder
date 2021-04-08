from unittest import TestCase
from cdr_plugin_folder_to_folder.utils.testing.Direct_API_Server import Direct_API_Server
from os import environ

class test_Configure_Env(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Direct_API_Server().setup()
        cls.prefix = 'configaration'

    def test_reset(self):
        path = f"{self.prefix}/reset"
        response = self.client.POST(path)
        assert response is not None
        self.assertEqual(response ,"Reset Completed")

    def test_configure(self):
        path = f"{self.prefix}/configure_env/"
        response = self.client.POST(
            path,
            json={'hd1_path': './test_data/scenario-1/hd1','hd2_path': './test_data/scenario-1/hd2','hd3_path': './test_data/scenario-1/hd3','gw_address': '127.0.0.1','gw_port': '8000'},
        )
        assert response is not None
        assert response == {
                      "hd1_path": "./test_data/scenario-1/hd1",
                      "hd2_path": "./test_data/scenario-1/hd2",
                      "hd3_path": "./test_data/scenario-1/hd3",
                      "gw_address": "127.0.0.1",
                      "gw_port": "8000"
                    }
        if "MODE" in environ:
            del environ["MODE"]










