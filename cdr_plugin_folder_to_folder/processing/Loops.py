import os
import os.path
import sys
import threading
import asyncio

from osbot_utils.utils.Files import create_folder, folder_exists

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.processing.Events_Log import Events_Log
from cdr_plugin_folder_to_folder.processing.File_Processing import File_Processing
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.pre_processing.Status import Status, FileStatus
from cdr_plugin_folder_to_folder.pre_processing.Hash_Json import Hash_Json

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
        self.config = Config()
        self.status = Status()
        self.hash_json = Hash_Json()
        self.hash_json.get_from_file()
        self.events = Events_Log(os.path.join(self.config.hd2_location, "status"))
        self.hash=None

    def IsProcessing(self):
        return Loops.processing_started

    def StopProcessing(self):
        Loops.continue_processing = False

    def HasBeenStopped(self):
        return not Loops.continue_processing

    @log_duration
    def ProcessDirectoryWithEndpoint(self, itempath, file_hash, endpoint_index):
        meta_service = Metadata_Service()
        original_file_path = meta_service.get_original_file_paths(itempath)
        events = Events_Log(itempath)

        endpoint = "http://" + self.config.endpoints['Endpoints'][endpoint_index]['IP'] + ":" + self.config.endpoints['Endpoints'][endpoint_index]['Port']
        events.add_log("Processing with: " + endpoint)

        if os.path.isdir(itempath):
            try:
                file_processing = File_Processing(events)
                if not file_processing.processDirectory(endpoint, itempath):
                    events.add_log("CANNOT be processed")
                    return False

                log_data = {
                        'file': original_file_path,
                        'status': FileStatus.COMPLETED.value,
                        'error': 'none',
                        'timestamp': datetime.now(),
                    }
                log_info('ProcessDirectoryWithEndpoint', data=log_data)
                meta_service.set_error(itempath, "none")
                meta_service.set_status(itempath, FileStatus.COMPLETED.value)
                self.status.add_completed()
                self.hash_json.update_status(file_hash, FileStatus.COMPLETED.value)
                events.add_log("Has been processed")
                return True
            except Exception as error:
                log_data = {
                    'file': original_file_path,
                    'status': FileStatus.FAILED.value,
                    'error': str(error),
                }
                log_error('error in ProcessDirectoryWithEndpoint', data=log_data)
                meta_service.set_error(itempath, str(error))
                meta_service.set_status(itempath, FileStatus.FAILED.value)
                self.status.add_failed()
                self.hash_json.update_status(file_hash, FileStatus.FAILED.value)
                events.add_log("ERROR:" + str(error))
                return False

    @log_duration
    def ProcessDirectory(self, itempath, file_hash, process_index):
        endpoint_index = process_index % self.config.endpoints_count
        for idx in range(self.config.endpoints_count):
            if self.ProcessDirectoryWithEndpoint(itempath, file_hash, endpoint_index):
                return
            # The Endpoint failed to process the file
            # Retry it with the next one
            endpoint_index = (endpoint_index + 1) % self.config.endpoints_count

    @log_duration
    def LoopHashDirectoriesInternal(self, thread_count, do_single):

        if not isinstance(thread_count,int):
            raise TypeError("thread_count must be a integer")

        if not isinstance(do_single,bool):
            raise TypeError("thread_count must be a integer")

        self.events.add_log("LoopHashDirectoriesAsync started")

        self.hash_json.get_from_file()

        rootdir = os.path.join(self.config.hd2_location, "data")

        if folder_exists(rootdir) is False:
            log_error("ERROR: rootdir does not exist: " + rootdir)
            return

        threads = list()

        json_list       = self.hash_json.get_json_list()
        process_index   = 0

        for key in json_list:
            file_hash   =  key

            itempath = os.path.join(rootdir, key)
            if (FileStatus.INITIAL.value != json_list[key]["file_status"]):
                continue

            if not os.path.exists(itempath):
                json_list[key]["file_status"] = FileStatus.FAILED.value
                continue

            # limit the number of parallel threads
            if process_index % int(thread_count) == 0:
                # Clean up the threads
                for index, thread in enumerate(threads):
                    thread.join()

            process_index += 1
            x = threading.Thread(target=self.ProcessDirectory, args=(itempath, file_hash, process_index,))
            threads.append(x)
            x.start()

            if do_single:
                break

            if not Loops.continue_processing:
                break

        for index, thread in enumerate(threads):
            thread.join()

        self.events.add_log("LoopHashDirectoriesAsync finished")

    @log_duration
    async def LoopHashDirectoriesAsync(self, thread_count, do_single = False):
        await Loops.lock.acquire()
        try:
            Loops.continue_processing = True
            Loops.processing_started = True

            self.LoopHashDirectoriesInternal(thread_count, do_single)
        finally:
            Loops.processing_started = False
            Loops.lock.release()
            self.status.write_to_file()

    @log_duration
    def LoopHashDirectories(self):
        #Allow only a single loop to be run at a time
        if self.IsProcessing():
            log_error("ERROR: Attempt to start processing while processing is in progress")
            return False

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.LoopHashDirectoriesAsync(self.config.thread_count))
        return True

    @log_duration
    def LoopHashDirectoriesSequential(self):
        #Allow only a single loop to be run at a time
        if self.IsProcessing():
            log_error("ERROR: Attempt to start processing while processing is in progress")
            return False

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.LoopHashDirectoriesAsync(1))
        return True

    @log_duration
    def ProcessSingleFile(self):
        if self.IsProcessing():
            log_error("ERROR: Attempt to start processing while processing is in progress")
            return False

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.LoopHashDirectoriesAsync(1, True))
        return True
