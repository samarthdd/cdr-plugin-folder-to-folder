import threading
from IPython.display import display
import ipywidgets as widgets
from IPython.display import clear_output
import ipywidgets as widgets
import time 
from datetime import datetime

class Show_progress:
    def __init__(self, api):
        self.event = threading.Event()
        self.api=api
        self.start_time=datetime.now()
        self.end_time  =None
        self.time_taken=None
        
    def start(self):
        
        status= self.api.get_processing_status()

        max   = status["files_to_process"]
        value = status ["completed"] + status ["failed"]
            
        if max == value and max != 0:
            self.event.set()
            self.end_time=datetime.now()
            
            self.time_taken = self.end_time-self.start_time
            display("Processing is completed")
            
        progress_bar  = self.show_progress(max,value)
        
        if self.time_taken :
            display(f"Total time taken : {self.time_taken}")

        display(status)
        display(progress_bar)
       
        if not self.event.is_set():
            threading.Timer(2, self.start).start()
            clear_output(wait=True)
            
    def stop(self):
        self.event.set()
        self.end_time=datetime.now()
        time.sleep(8)
        
    def show_progress(self,max,value):
        progress_bar = widgets.IntProgress(min=0, max=max, description='Progress Bar:', bar_style='info', )
        progress_bar.value = value
        return progress_bar
