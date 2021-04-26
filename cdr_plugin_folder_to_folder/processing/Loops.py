import os
import os.path
import sys
import threading
import asyncio
import subprocess
from multiprocessing.pool import ThreadPool

from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Files import create_folder, folder_exists

from cdr_plugin_folder_to_folder.common_settings.Config import Config, API_VERSION
from cdr_plugin_folder_to_folder.processing.Events_Log import Events_Log
from cdr_plugin_folder_to_folder.processing.File_Processing import File_Processing
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.pre_processing.Status import Status, FileStatus
from cdr_plugin_folder_to_folder.pre_processing.Hash_Json import Hash_Json
from cdr_plugin_folder_to_folder.processing.Report_Elastic import Report_Elastic

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
        self.report_elastic = Report_Elastic()
        self.report_elastic.setup()

    def IsProcessing(self):
        return Loops.processing_started

    def StopProcessing(self):
        Loops.continue_processing = False

    def HasBeenStopped(self):
        return not Loops.continue_processing

    def git_commit(self):
        git_commit = 'Not available'
        try:
            git_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode("utf-8").rstrip()
        except Exception as e:
            pass

        return git_commit

    def ProcessDirectoryWithEndpoint(self, itempath, file_hash, endpoint_index):
        log_info(message=f"Starting ProcessDirectoryWithEndpoint on endpoint # {endpoint_index} for file {file_hash}")
        meta_service = Metadata_Service()
        original_file_path = meta_service.get_original_file_paths(itempath)
        events = Events_Log(itempath)

        endpoint = "http://" + self.config.endpoints['Endpoints'][endpoint_index]['IP'] + ":" + self.config.endpoints['Endpoints'][endpoint_index]['Port']
        events.add_log("Processing with: " + endpoint)

        meta_service.set_f2f_plugin_version(itempath, API_VERSION)
        meta_service.set_f2f_plugin_git_commit(itempath, self.git_commit())

        if os.path.isdir(itempath):
            try:
                file_processing = File_Processing(events, self.report_elastic, meta_service)
                if not file_processing.processDirectory(endpoint, itempath):
                    events.add_log("CANNOT be processed")
                    return False

                log_data = {
                        'file': original_file_path,
                        'status': FileStatus.COMPLETED,
                        'error': 'none',
                        'timestamp': datetime.now(),
                    }
                log_info('ProcessDirectoryWithEndpoint', data=log_data)
                #meta_service.set_error(itempath, "none")
                #meta_service.set_status(itempath, FileStatus.COMPLETED)
                self.status.add_completed()
                #self.hash_json.update_status(file_hash, FileStatus.COMPLETED)
                events.add_log("Has been processed")
                return True
            except Exception as error:
                log_data = {
                    'file': original_file_path,
                    'status': FileStatus.FAILED,
                    'error': str(error),
                }
                log_error(message='error in ProcessDirectoryWithEndpoint', data=log_data)
                meta_service.set_error(itempath, str(error))
                meta_service.set_status(itempath, FileStatus.FAILED)
                self.status.add_failed()
                self.hash_json.update_status(file_hash, FileStatus.FAILED)
                events.add_log("ERROR:" + str(error))
                return False


    def ProcessDirectory(self, thread_data):
        (itempath, file_hash, process_index) = thread_data
        endpoint_index = process_index % self.config.endpoints_count
        if not Loops.continue_processing:
            return False
        return self.ProcessDirectoryWithEndpoint(itempath, file_hash, endpoint_index)

        # note: removing retries from this method (it should not be handled like this
        #for idx in range(self.config.endpoints_count):
        #    if self.ProcessDirectoryWithEndpoint(itempath, file_hash, endpoint_index):
        #        return
        #    # The Endpoint failed to process the file
        #    # Retry it with the next one
        #    endpoint_index = (endpoint_index + 1) % self.config.endpoints_count

    def LoopHashDirectoriesInternal(self, thread_count, do_single):

        if not isinstance(thread_count,int):
            raise TypeError("thread_count must be a integer")

        if not isinstance(do_single,bool):
            raise TypeError("thread_count must be a integer")

        log_info(f"LoopHashDirectoriesAsync started with {thread_count} threads")

        json_list = self.hash_json.get_from_file()

        log_info(f"There are {len(json_list)} files to in hash_json (i.e. to review) ")

        rootdir = os.path.join(self.config.hd2_location, "data")

        if folder_exists(rootdir) is False:
            log_error("ERROR: rootdir does not exist: " + rootdir)
            return

        threads = list()

        process_index   = 0

        log_info(message=f'before Mapping thread_data for {len(json_list)} files')
        thread_data = []
        for key in json_list:
            file_hash   =  key

            itempath = os.path.join(rootdir, key)
            if (FileStatus.INITIAL != json_list[key]["file_status"]):
                continue

            if not os.path.exists(itempath):
                json_list[key]["file_status"] = FileStatus.FAILED
                continue

            process_index += 1
            thread_data.append((itempath, file_hash, process_index,))
            # # limit the number of parallel threads
            #
            # if process_index % int(thread_count) == 0:                      # todo: refactor this workflow to use multiprocess and queues
            #     # Clean up the threads
            #     for index, thread in enumerate(threads):                    # todo: since at the moment this will block allocating new threads until
            #         thread.join()                                           #       all have finishing execution
            #
            # process_index += 1
            # log_info(message=f"in LoopHashDirectoriesInternal process_index={process_index} , thread #{process_index % int(thread_count) }")
            # x = threading.Thread(target=self.ProcessDirectory, args=(itempath, file_hash, process_index,))
            # threads.append(x)
            # x.start()
            #
            # if do_single:
            #     break
            #
            # if not Loops.continue_processing:
            #     break

        # for index, thread in enumerate(threads):
        #     thread.join()

        log_info(message=f'after mapped thread_data, there are {len(thread_data)} mapped items')
        thread_data = thread_data[:50]
        log_info(message=f'to start with only processing {len(thread_data)} thread_data items')
        pool = ThreadPool(thread_count)
        results = pool.map(self.ProcessDirectory, thread_data)
        pool.close()
        pool.join()

        self.events.add_log("LoopHashDirectoriesAsync finished")
        return results

    async def LoopHashDirectoriesAsync(self, thread_count, do_single = False):
        await Loops.lock.acquire()
        try:
            Loops.continue_processing = True
            Loops.processing_started = True

            self.LoopHashDirectoriesInternal(thread_count, do_single)
        finally:
            Loops.processing_started = False
            Loops.lock.release()
            self.status.save()

    @log_duration
    def LoopHashDirectories(self):
        #Allow only a single loop to be run at a time
        if self.IsProcessing():
            log_error(message="ERROR: Attempt to start processing while processing is in progress")
            return False
        log_info(message="in LoopHashDirectories, about to start main loop")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.LoopHashDirectoriesAsync(self.config.thread_count))
        log_info(message="in LoopHashDirectories, Loop completed")
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
