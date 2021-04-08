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

    @staticmethod
    def ProcessDirectory(endpoint, itempath, idx, use_es, es):
        meta_service = Metadata_Service()
        original_file_path = meta_service.get_original_file_path(itempath)
        if os.path.isdir(itempath):
            try:
                File_Processing.processDirectory(endpoint, itempath)
                if use_es:
                    log = {
                        'file': original_file_path,
                        'status': 'processed',
                        'error': 'none',
                        'timestamp': datetime.now(),
                    }
                    es.index(index='processed-index', id=idx, body=log)
                meta_service.set_error(itempath, "none")
            except Exception as error:
                if use_es:
                    log = {
                        'file': original_file_path,
                        'status': 'failed',
                        'error': str(error),
                        'timestamp': datetime.now(),
                    }
                    es.index(index='processed-index', id=idx, body=log)
                meta_service.set_error(itempath, str(error))

    @staticmethod
    def LoopHashDirectories():
        config = Config().load_values()
        rootdir = os.path.join(config.hd2_location,"data")
        directory_contents = os.listdir(rootdir)

        es = Elasticsearch()
        use_es = False

        try:
            es = Elasticsearch([{'host': config.elastic_host, 'port': int(config.elastic_port)}])
            # ignore 400 cause by IndexAlreadyExistsException when creating an index
            es.indices.create(index='processed-index', ignore=400)
            use_es = True
        except Exception as error:
            print("The connection to Elastic cannot be established")

        files_count = 0
        threads = list()

        for item in directory_contents:
            files_count += 1
            itempath = os.path.join(rootdir,item)
            #Loops.ProcessDirectory(itempath, idx, use_es, es)

            endpoint = "http://" + config.endpoints['Endpoints'][0]['IP'] + ":" + config.endpoints['Endpoints'][0]['Port']

            x = threading.Thread(target=Loops.ProcessDirectory, args=(endpoint, itempath, files_count, use_es, es,))
            threads.append(x)
            x.start()
            # limit the number of parallel threads
            if files_count % int(config.thread_count) == 0:
                # Clean up the threads
                #logging.info ('Files processed so far {}'.format(files_count))
                for index, thread in enumerate(threads):
                    thread.join()

        for index, thread in enumerate(threads):
            thread.join()
