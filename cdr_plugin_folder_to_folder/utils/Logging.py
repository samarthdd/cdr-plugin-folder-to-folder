import inspect
from datetime import datetime

from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import timestamp_utc_now, date_now, date_time_now

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.utils.Elastic import Elastic

DEFAULT_LOGS_INDEX_NAME = 'application_logs'

class Logging:

    def __init__(self, index_name=DEFAULT_LOGS_INDEX_NAME):
        #self.config        = Config()
        self.index_name    = index_name
        self.time_field    = 'timestamp'
        self.refresh_index = False
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

    def get_logs(self):
        return self.elastic().get_data()

    def set_refresh_index(self, value):
        self.refresh_index = value
        return self


    # main logging methods

    def log_message(self, level, message=None, data=None, duration='', from_method=None, from_class=None, caller_depth=3):
        stack       = inspect.stack()                                                               # todo: refactor into separate method/class
        from_class  = from_class  or stack[caller_depth][0].f_locals["self"].__class__.__name__     # todo: handle case when self doesn't exist
        from_method = from_method or stack[caller_depth][0].f_code.co_name

        data = { "duration"     : duration      ,
                 "from_class"   : from_class    ,
                 "from_method"  : from_method   ,
                 "level"        : level         ,
                 "message"      : message       ,
                 "data"         : data          ,
                 self.time_field: datetime.utcnow()}
        if self.enabled:
            return self.elastic().add(data=data, refresh=self.refresh_index)
        # if elastic server is not available, log messages to console
        pprint(data)

    def critical(self, message, data=None, duration=''):  return self.log_message("CRITICAL", message ,data=data, duration=duration)
    def debug   (self, message, data=None, duration=''):  return self.log_message("DEBUG"   , message ,data=data, duration=duration)
    def error   (self, message, data=None, duration=''):  return self.log_message("ERROR"   , message ,data=data, duration=duration)
    def info    (self, message, data=None, duration=''):  return self.log_message("INFO"    , message ,data=data, duration=duration)
    def warning (self, message, data=None, duration=''):  return self.log_message("WARNING" , message ,data=data, duration=duration)


logging = Logging().setup()             # todo: refactor this so that the constructor is not invoked here

def log_message (*args, **kwargs):  return logging.log_message(*args, **kwargs)     # helper static logging classes

def log_critical(*args, **kwargs):  return logging.critical (*args, **kwargs)
def log_debug   (*args, **kwargs):  return logging.debug    (*args, **kwargs)
def log_error   (*args, **kwargs):  return logging.error    (*args, **kwargs)
def log_info    (*args, **kwargs):  return logging.info     (*args, **kwargs)
def log_warning (*args, **kwargs):  return logging.warning  (*args, **kwargs)