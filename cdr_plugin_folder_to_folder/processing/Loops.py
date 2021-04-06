import os
import os.path
import sys

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.processing.File_Processing import File_Processing
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service

from elasticsearch import Elasticsearch
from datetime import datetime

class Loops(object):

    @staticmethod
    def LoopHashDirectories():
        config = Config().load_values()
        rootdir = os.path.join(config.hd2_location,"data")
        directory_contents = os.listdir(rootdir)
        meta_service = Metadata_Service()

        es = Elasticsearch()
        use_es = False

        try:
            es = Elasticsearch([{'host': config.elastic_host, 'port': int(config.elastic_port)}])
            # ignore 400 cause by IndexAlreadyExistsException when creating an index
            es.indices.create(index='processed-index', ignore=400)
            use_es = True
        except Exception as error:
            print("The connection to Elastic cannot be established")

        idx = 0
        for item in directory_contents:
            idx += 1
            itempath = os.path.join(rootdir,item)
            original_file_path = meta_service.get_original_file_path(itempath)
            if os.path.isdir(itempath):
                try:
                    File_Processing.processDirectory(itempath)
                    if use_es:
                        log = {
                            'file': original_file_path,
                            'status': 'processed',
                            'error': 'none',
                            'timestamp': datetime.now(),
                        }
                        es.index(index='processed-index', id=idx, body=log)
                except Exception as error:
                    if use_es:
                        log = {
                            'file': original_file_path,
                            'status': 'failed',
                            'error': str(error),
                            'timestamp': datetime.now(),
                        }
                        es.index(index='processed-index', id=idx, body=log)
                    print(error)