import sys
import uvicorn
from fastapi import FastAPI
from cdr_plugin_folder_to_folder.processing.Loops import Loops
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor

app = FastAPI()

@app.get("/")
def read_root():
    return "FastAPI Home"

@app.get("/loop")
def run_the_loop():
    Loops.LoopHashDirectories()
    return "Loop completed"

@app.get("/pre-process")
def start_process():
    pre_processor = Pre_Processor()
    pre_processor.process_files()
    return {"Processing is done"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, log_level="info")