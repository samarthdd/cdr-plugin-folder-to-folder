import multiprocessing
from time import sleep
from typing import Tuple
from unittest import TestCase
from unittest.mock import patch

import pytest
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import random_text

from cdr_plugin_folder_to_folder.utils.Elastic import Elastic
from cdr_plugin_folder_to_folder.utils.Logging import log_info, log_error, logging_queue, log_message, logging_enabled, \
    log_warning, logging_counter, log_debug
from cdr_plugin_folder_to_folder.utils.Logging_Process import start_logging_process, start_logging
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing


class test_Logging_Process(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        Setup_Testing().pytest_skip_if_elastic_not_available()

    def setUp(self) -> None:
        pass

    def test__start_logging(self):
        # todo: understand better why this test takes about 1.1 secs to execute (some of it is caused by the processing process starting, and elastic being setup)
        log_worker = start_logging()                                        # trigger logging process
        log_info()                                                      # send 4 log messages
        log_warning()
        log_info(message=random_text(), data={'a': 42})
        log_error(message='an error')
        # todo: improve test to actually read messages from elastic and confirm they made it ok
        #log_message(level="self.level", message="self.message", duration="message_duration", from_class="self.from_class",
        #            from_method="self.from_method")

        counter = logging_counter                   # get counter

        log_debug(message='stop_logging', data={'when': 'now'})
        log_worker.join()

        #while counter.value != 4:                   # wait for the 4 messages being processed
        #    worker.join(timeout=0.1)                # join worker process to give it time to execute
