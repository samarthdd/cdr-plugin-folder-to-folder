import os
import os.path
import sys
import threading
import asyncio

from osbot_utils.utils.Files import create_folder, folder_exists

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.processing.File_Processing import File_Processing
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.pre_processing.Status import Status
from cdr_plugin_folder_to_folder.pre_processing.Status import FileStatus

from elasticsearch import Elasticsearch
from datetime import datetime

from cdr_plugin_folder_to_folder.utils.Log_Duration import log_duration
from cdr_plugin_folder_to_folder.utils.Logging import log_error, log_info


class Loops(object):

    continue_processing = False
    processing_started = False
    lock = asyncio.Lock()

    def __init__(self):
        self.use_es = False
        self.config = Config().load_values()
        self.status = Status()
        self.status.get_from_file()

    def IsProcessing(self):
        return Loops.processing_started

    def StopProcessing(self):
        Loops.continue_processing = False

    def HasBeenStopped(self):
        return not Loops.continue_processing

    @log_duration
    def ProcessDirectoryWithEndpoint(self, itempath, file_index, endpoint_index):
        self.config = Config().load_values()
        meta_service = Metadata_Service()
        original_file_path = meta_service.get_original_file_path(itempath)
        file_processing = File_Processing()

        endpoint = "http://" + self.config.endpoints['Endpoints'][endpoint_index]['IP'] + ":" + self.config.endpoints['Endpoints'][endpoint_index]['Port']

        if os.path.isdir(itempath):
            try:
                result = file_processing.processDirectory(endpoint, itempath)
                log_data = {
                        'file': original_file_path,
                        'status': FileStatus.COMPLETED.value,
                        'error': 'none',
                        'timestamp': datetime.now(),
                    }
                log_info('ProcessDirectoryWithEndpoint', data=log_data)
                meta_service.set_error(itempath, "none")
                meta_service.set_status(FileStatus.COMPLETED.value)
                return result
            except Exception as error:
                log_data = {
                    'file': original_file_path,
                    'status': FileStatus.FAILED.value,
                    'error': str(error),
                }
                log_error('error in ProcessDirectoryWithEndpoint', data=log_data)
                meta_service.set_error(itempath, str(error))
                meta_service.set_status(itempath, FileStatus.FAILED.value)
                return False

    @log_duration
    def ProcessDirectory(self, itempath, file_index, process_index):
        self.config = Config().load_values()
        endpoint_index = process_index % self.config.endpoints_count
        for idx in range(self.config.endpoints_count):
            if self.ProcessDirectoryWithEndpoint(itempath, file_index, endpoint_index):
                return True
            # The Endpoint failed to process the file
            # Retry it with the next one
            endpoint_index = (endpoint_index + 1) % self.config.endpoints_count
        return False

    @log_duration
    def LoopHashDirectoriesInternal(self, thread_count, do_single = False):

        rootdir = os.path.join(self.config.hd2_location, "data")

        if folder_exists(rootdir) is False:
            log_error("ERROR: rootdir does not exist: " + rootdir)
            return

        file_index = 0
        threads = list()

        file_list = self.status.get_file_list()
        process_index = 0

        for index in range(len(file_list)):

            if file_list[index]["file_status"] != FileStatus.INITIAL.value:
                continue

            process_index += 1
            itempath = os.path.join(rootdir,file_list[index]["hash"])
            file_index = file_list[index]["id"]

            x = threading.Thread(target=self.ProcessDirectory, args=(itempath, file_index, process_index,))
            threads.append(x)
            x.start()

            if do_single:
                break

            # limit the number of parallel threads
            if file_index % int(thread_count) == 0:
                # Clean up the threads
                for index, thread in enumerate(threads):
                    thread.join()

            if not Loops.continue_processing:
                break

        for index, thread in enumerate(threads):
            thread.join()

    @log_duration
    async def LoopHashDirectoriesAsync(self):
        await Loops.lock.acquire()
        try:
            Loops.continue_processing = True
            Loops.processing_started = True

            self.LoopHashDirectoriesInternal(self.config.thread_count)
        finally:
            Loops.processing_started = False
            Loops.lock.release()

    @log_duration
    def LoopHashDirectories(self):
        #Allow only a single loop to be run at a time
        if self.IsProcessing():
            log_error("ERROR: Attempt to start processing while processing is in progress")
            return False

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.LoopHashDirectoriesAsync())
        return True

    @log_duration
    def ProcessSingleFile(self):
        self.LoopHashDirectoriesInternal(1, True)

