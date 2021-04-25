import multiprocessing
from multiprocessing import Value
from multiprocessing.queues import Queue
from time import sleep

from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.utils.Logging import logging_queue, logging_enabled, Logging, log_info, log_debug

logging_process               = None
logging_worker                = None
delete_existing_elastic_index = False
print_log_messages            = False

def start_logging():
    global logging_worker
    queue   = logging_queue
    enabled = logging_enabled
    if logging_worker is None and logging_enabled.value ==0:       # if it already enabled don't start a new process
        worker = multiprocessing.Process(target=start_logging_process, args=(queue, enabled), daemon=True)
        worker.start()
        logging_enabled.value = 1       # set enabled value
        logging_worker = worker
        log_info(message="Logging Process started")
    return logging_worker


def start_logging_process(queue: Queue, enabled: Value):
    global logging_process
    logging_process = Logging_Process(queue=queue, enabled=enabled)
    pprint('>> start_logging_process')
    logging_process.start()

# use this method during development to wait for log entries to be sent to elastic (with it the tests will end before the logs have been captured)
def process_all_log_entries_and_end_logging_process():
    global logging_worker
    log_debug(message='stop_logging', data={'when': 'now'})
    logging_worker.join()

# def log_process(queue,record):
#
#     pprint(f'putting log:{record}')
#     queue.put_nowait(record)

class Logging_Process:

    def __init__(self, queue : Queue, enabled: Value):
        self._enabled = enabled
        self._queue   = queue
        self._logging = None
        self.setup()

    def enabled(self):
        return self._enabled.value == 1

    def queue(self):
        return self._queue

    def next_value(self):
        return self.queue().get()

    def logging(self):
        return self._logging

    def log_message(self, **kwargs):
        self.logging().log_message(**kwargs)

    def setup(self):
        #from cdr_plugin_folder_to_folder.utils.Logging import Logging
        self._logging = Logging()
        self._logging.setup(delete_existing=delete_existing_elastic_index)
        #set_logging_queue(self.queue())     # required to that we can add log messages from current process

    def start(self):
        while self.enabled():
            log_data = self.next_value()
            kwargs = {  "level"        : log_data.get("level"       ),
                        "message"      : log_data.get("message"     ),
                        "data"         : log_data.get("data"        ),
                        "duration"     : log_data.get("duration"    ),
                        "from_method"  : log_data.get("from_method" ),
                        "from_class"   : log_data.get("from_class"  )}

            if print_log_messages:
                pprint(kwargs)
            self.log_message(**kwargs)

            # todo refactor into method focused on internal logging messages
            if  kwargs.get('level'  ) == 'DEBUG'        and  \
                kwargs.get('message') == 'stop_logging' and  \
                kwargs.get('data'   ) == {'when' : 'now'}:
                return

    def queue_empty(self):
        return self.queue().empty()

    def queue_not_empty(self):
        return self.queue_empty() is False




