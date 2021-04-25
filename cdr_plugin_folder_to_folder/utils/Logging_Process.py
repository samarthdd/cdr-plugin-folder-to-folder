import multiprocessing
from multiprocessing import Value
from multiprocessing.queues import Queue
from time import sleep

from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.utils.Logging import logging_queue, logging_enabled, Logging, logging_counter

logging_process               = None
delete_existing_elastic_index = False
print_log_messages            = False

def start_logging():
    queue   = logging_queue
    enabled = logging_enabled
    count   = logging_counter
    pprint(f'logging_enabled.value: {logging_enabled.value}')
    if logging_enabled.value ==0:       # if it already enabled don't start a new process
        worker = multiprocessing.Process(target=start_logging_process, args=(queue, enabled, count), daemon=True)
        worker.start()
        logging_enabled.value = 1       # set enabled value
        return worker


def start_logging_process(queue: Queue, enabled: Value, count: Value):
    global logging_process
    logging_process = Logging_Process(queue=queue, enabled=enabled, count=count)
    pprint('>> start_logging_process')
    logging_process.start()

# def log_process(queue,record):
#
#     pprint(f'putting log:{record}')
#     queue.put_nowait(record)

class Logging_Process:

    def __init__(self, queue : Queue, enabled: Value, count: Value):
        self._count   = count
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

            with self._count.get_lock():
                self._count.value += 1
            # todo refactor into method focused on internal logging messages
            if  kwargs.get('level'  ) == 'DEBUG'        and  \
                kwargs.get('message') == 'stop_logging' and  \
                kwargs.get('data'   ) == {'when' : 'now'}:
                return

    def queue_empty(self):
        return self.queue().empty()

    def queue_not_empty(self):
        return self.queue_empty() is False




