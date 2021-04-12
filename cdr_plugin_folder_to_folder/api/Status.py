from osbot_utils.utils.Misc import datetime_now

from cdr_plugin_folder_to_folder.common_settings.Config import Config


class Status:

    def __init__(self):
        self.config = Config().load_values()

    def now(self):
        data = {
            "config": {
                "elastic" : f"{self.config.elastic_schema}://{self.config.elastic_host}:{self.config.elastic_port}",
                "kibana"  : f"{self.config.elastic_schema}://{self.config.kibana_host }:{self.config.kibana_port }"
            },
            "date": datetime_now()
        }

        return data