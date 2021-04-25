import inspect
from datetime import datetime
from multiprocessing import Queue, Value
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Dev import pprint
from cdr_plugin_folder_to_folder.utils.Elastic import Elastic

DEFAULT_LOGS_INDEX_NAME = 'application_logs'

class Logging:

    def __init__(self, index_name=DEFAULT_LOGS_INDEX_NAME):
        #self.config        = Config()
        self.index_name    = index_name
        self.time_field    = 'timestamp'
        self.refresh_index = False                              # set to true to delay the response from adding data until the data has been indexed (by Elastic)
        self.enabled       = False

    @cache_on_self
    def elastic(self):
        return Elastic(index_name=self.index_name, time_field=self.time_field)

    def setup(self, delete_existing=False):
        elastic = self.elastic()
        elastic.setup()
        if elastic.enabled:
            elastic.create_index_and_index_pattern(delete_existing=delete_existing)
            self.enabled = True
        return self

    # def get_logs(self):
    #     return self.elastic().get_data()

    def set_refresh_index(self, value):
        self.refresh_index = value
        return self


    # main logging methods

    def log_message(self, level='INFO', message=None, data=None, duration='', from_method=None, from_class=None):
        if type(data) is str:
            data = {'str': data }                                   # so that elastic doesn't make this field a string

        log_data = { "duration"     : duration         ,
                     "from_class"   : from_class       ,
                     "from_method"  : from_method      ,
                     "level"        : level            ,
                     "message"      : message          ,
                     "data"         : data             ,
                     self.time_field: datetime.utcnow()}           # this is a python datatime object (which is well supported by elastic but doesn't serialise to json ok)
        if self.enabled:
            return self.elastic().add(data=log_data, refresh=self.refresh_index)
        # if elastic server is not available, log messages to console
        pprint(log_data)

    def critical(self, message, data=None, duration=''):  return self.log_message("CRITICAL", message ,data=data, duration=duration)
    def debug   (self, message, data=None, duration=''):  return self.log_message("DEBUG"   , message ,data=data, duration=duration)
    def error   (self, message, data=None, duration=''):  return self.log_message("ERROR"   , message ,data=data, duration=duration)
    def info    (self, message, data=None, duration=''):  return self.log_message("INFO"    , message ,data=data, duration=duration)
    def warning (self, message, data=None, duration=''):  return self.log_message("WARNING" , message ,data=data, duration=duration)

# helper static logging classes

logging_queue   = Queue()
logging_enabled = Value('i', 0)

def set_logging_queue(queue):           # use to enabled multiple process to send logging messages to a particular queue
    global logging_queue
    logging_queue = queue

def calculate_from_method(from_method,caller_depth=2):

    if from_method:
        return from_method
    try:
        stack = inspect.stack(0)
        return  stack[caller_depth][0].f_code.co_name
    except:
        return 'NA'

def calculate_from_class(from_class, caller_depth=2):
    if from_class:
        return from_class
    try:
        stack = inspect.stack(0)
        return stack[caller_depth][0].f_locals["self"].__class__.__name__     # todo: handle case when self doesn't exist
    except:
        return 'NA'

def log_message (level=None, message=None, data=None, duration=0, from_method=None, from_class=None):  return logging_queue.put_nowait ({"level":level    , "message":message, "data":data, "duration":duration, "from_method":calculate_from_method(from_method), "from_class":calculate_from_class(from_class)})

def log_critical(            message=None, data=None, duration=0, from_method=None, from_class=None):  return logging_queue.put_nowait({"level":"CRITICAL", "message":message, "data":data, "duration":duration, "from_method":calculate_from_method(from_method), "from_class":calculate_from_class(from_class)})
def log_debug   (            message=None, data=None, duration=0, from_method=None, from_class=None):  return logging_queue.put_nowait({"level":"DEBUG"   , "message":message, "data":data, "duration":duration, "from_method":calculate_from_method(from_method), "from_class":calculate_from_class(from_class)})
def log_error   (            message=None, data=None, duration=0, from_method=None, from_class=None):  return logging_queue.put_nowait({"level":"ERROR"   , "message":message, "data":data, "duration":duration, "from_method":calculate_from_method(from_method), "from_class":calculate_from_class(from_class)})
def log_info    (            message=None, data=None, duration=0, from_method=None, from_class=None):  return logging_queue.put_nowait({"level":"INFO"    , "message":message, "data":data, "duration":duration, "from_method":calculate_from_method(from_method), "from_class":calculate_from_class(from_class)})
def log_warning (            message=None, data=None, duration=0, from_method=None, from_class=None):  return logging_queue.put_nowait({"level":"WARNING" , "message":message, "data":data, "duration":duration, "from_method":calculate_from_method(from_method), "from_class":calculate_from_class(from_class)})