import sys
from fastapi import FastAPI
import uvicorn
from file_iteration import Loops

sys.path.insert(1, '../pre_processing')
sys.path.insert(1, '../pre_processing/utils')
from Pre_Processor import Pre_Processor

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
    uvicorn.run("main:app", host="127.0.0.1", port=80, log_level="info")