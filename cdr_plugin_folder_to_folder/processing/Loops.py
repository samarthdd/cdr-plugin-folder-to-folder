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

    es = Elasticsearch()
    use_es = False
    config = Config().load_values()

    @staticmethod
    def ProcessDirectoryWithEndpoint(itempath, file_index, endpoint_index):
        Loops.config = Config().load_values()
        print(Loops.config.endpoints)
        meta_service = Metadata_Service()
        original_file_path = meta_service.get_original_file_path(itempath)

        endpoint = "http://" + Loops.config.endpoints['Endpoints'][endpoint_index]['IP'] + ":" + Loops.config.endpoints['Endpoints'][endpoint_index]['Port']

        if os.path.isdir(itempath):
            try:
                File_Processing.processDirectory(endpoint, itempath)
                if Loops.use_es:
                    log = {
                        'file': original_file_path,
                        'status': 'processed',
                        'error': 'none',
                        'timestamp': datetime.now(),
                    }
                    Loops.es.index(index='processed-index', id=file_index, body=log)
                meta_service.set_error(itempath, "none")
                return True
            except Exception as error:
                if Loops.use_es:
                    log = {
                        'file': original_file_path,
                        'status': 'failed',
                        'error': str(error),
                        'timestamp': datetime.now(),
                    }
                    Loops.es.index(index='processed-index', id=file_index, body=log)
                meta_service.set_error(itempath, str(error))
                return False

    @staticmethod
    def ProcessDirectory(itempath, file_index):
        Loops.config = Config().load_values()
        endpoint_index = file_index % Loops.config.endpoints_count
        for idx in range(Loops.config.endpoints_count):
            if Loops.ProcessDirectoryWithEndpoint(itempath, file_index, endpoint_index):
                break
            # The Endpoint failed to process the file
            # Retry it with the next one
            endpoint_index = (endpoint_index + 1) % Loops.config.endpoints_count

    @staticmethod
    def LoopHashDirectories():
        Loops.config = Config().load_values()
        rootdir = os.path.join(Loops.config.hd2_location,"data")
        directory_contents = os.listdir(rootdir)

        try:
            Loops.es = Elasticsearch([{'host': Loops.config.elastic_host, 'port': int(Loops.config.elastic_port)}])
            # ignore 400 cause by IndexAlreadyExistsException when creating an index
            Loops.es.indices.create(index='processed-index', ignore=400)
            Loops.use_es = True
        except Exception as error:
            Loops.es = Elasticsearch()
            Loops.use_es = False

        file_index = 0
        threads = list()

        for item in directory_contents:
            file_index += 1
            itempath = os.path.join(rootdir,item)

            x = threading.Thread(target=Loops.ProcessDirectory, args=(itempath, file_index,))
            threads.append(x)
            x.start()
            # limit the number of parallel threads
            if file_index % int(Loops.config.thread_count) == 0:
                # Clean up the threads
                for index, thread in enumerate(threads):
                    thread.join()

        for index, thread in enumerate(threads):
            thread.join()
