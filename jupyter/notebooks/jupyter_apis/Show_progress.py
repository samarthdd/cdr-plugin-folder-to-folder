import threading
from IPython.display import display
import ipywidgets as widgets
from IPython.display import clear_output
import ipywidgets as widgets
import time 

class Show_progress:
    def __init__(self, api):
        self.event = threading.Event()
        self.api=api
        
    def start(self):
        status= self.api.get_processing_status()

        max   = status["files_count"]
        value = status ["completed"] + status ["failed"]
        progress_bar  = self.show_progress(max,value)

        display(status)
        display(progress_bar)
       
        if not self.event.is_set():
            threading.Timer(2, self.start).start()
            clear_output(wait=True)
            
    def stop(self):
        self.event.set()
        time.sleep(8)
        
    def show_progress(self,max,value):
        progress_bar = widgets.IntProgress(min=0, max=max, description='Progress Bar:', bar_style='info', )
        progress_bar.value = value
        return progress_bar
