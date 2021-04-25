import functools
from functools import wraps

from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Misc import time_delta_to_str

from cdr_plugin_folder_to_folder.utils.Logging import log_message


def log_duration(function):

    #@wraps(function)
    @functools.wraps(function)
    def wrapper(*args,**kwargs):
        try:
            message = args[1]
        except:
            message = ''
        from_method = function.__name__
        from_class  = function.__module__.split('.').pop()
        with Log_Duration(message=message,from_method=from_method, from_class=from_class):
            return function(*args,**kwargs)

    return wrapper

class Log_Duration:

    def __init__(self, message, from_class=None, from_method=None):
        self.message      = message
        self.duration     = Duration(print_result=False)
        self.from_class   = from_class
        self.from_method  = from_method
        self.level        = 'INFO'

    def __enter__(self):
        self.duration.start()
        #log_info(self.message, context="Started", caller_depth=3)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration.end()
        #message_duration = time_delta_to_str(self.duration.duration)
        message_duration = self.duration.seconds()
        log_message(level=self.level, message=self.message, duration=message_duration, from_class=self.from_class, from_method=self.from_method)
