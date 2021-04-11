import os
import os.path
import sys
import threading

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.processing.File_Processing import File_Processing
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service

from elasticsearch import Elasticsearch
from datetime import datetime

class Loops(object):

    def __init__(self):
        self.es = Elasticsearch()
        self.use_es = False
        self.config = Config().load_values()

    def ProcessDirectoryWithEndpoint(self, itempath, file_index, endpoint_index):
        self.config = Config().load_values()
        print(self.config.endpoints)
        meta_service = Metadata_Service()
        original_file_path = meta_service.get_original_file_path(itempath)
        file_processing = File_Processing()

        endpoint = "http://" + self.config.endpoints['Endpoints'][endpoint_index]['IP'] + ":" + self.config.endpoints['Endpoints'][endpoint_index]['Port']

        if os.path.isdir(itempath):
            try:
                file_processing.processDirectory(endpoint, itempath)
                if self.use_es:
                    log = {
                        'file': original_file_path,
                        'status': 'processed',
                        'error': 'none',
                        'timestamp': datetime.now(),
                    }
                    self.es.index(index='processed-index', id=file_index, body=log)
                meta_service.set_error(itempath, "none")
                return True
            except Exception as error:
                if self.use_es:
                    log = {
                        'file': original_file_path,
                        'status': 'failed',
                        'error': str(error),
                        'timestamp': datetime.now(),
                    }
                    self.es.index(index='processed-index', id=file_index, body=log)
                meta_service.set_error(itempath, str(error))
                return False

    def ProcessDirectory(self, itempath, file_index):
        self.config = Config().load_values()
        endpoint_index = file_index % self.config.endpoints_count
        for idx in range(self.config.endpoints_count):
            if self.ProcessDirectoryWithEndpoint(itempath, file_index, endpoint_index):
                break
            # The Endpoint failed to process the file
            # Retry it with the next one
            endpoint_index = (endpoint_index + 1) % self.config.endpoints_count

    def LoopHashDirectories(self):
        self.config = Config().load_values()
        rootdir = os.path.join(self.config.hd2_location,"data")
        directory_contents = os.listdir(rootdir)

        try:
            self.es = Elasticsearch([{'host': self.config.elastic_host, 'port': int(self.config.elastic_port)}])
            # ignore 400 cause by IndexAlreadyExistsException when creating an index
            self.es.indices.create(index='processed-index', ignore=400)
            self.use_es = True
        except Exception as error:
            self.es = Elasticsearch()
            self.use_es = False

        file_index = 0
        threads = list()

        for item in directory_contents:
            file_index += 1
            itempath = os.path.join(rootdir,item)

            x = threading.Thread(target=self.ProcessDirectory, args=(itempath, file_index,))
            threads.append(x)
            x.start()
            # limit the number of parallel threads
            if file_index % int(self.config.thread_count) == 0:
                # Clean up the threads
                for index, thread in enumerate(threads):
                    thread.join()

        for index, thread in enumerate(threads):
            thread.join()
