import sys
import uvicorn
from fastapi import FastAPI
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor

#app = FastAPI()
from fastapi import APIRouter

from cdr_plugin_folder_to_folder.processing.Loops import Loops

router = APIRouter()

@router.get("/")
def read_root():
    return "FastAPI Home"

@router.get("/loop")
def run_the_loop():
    Loops.LoopHashDirectories()
    return "Loop completed"

#if __name__ == "__main__":
#    uvicorn.run("main:app", host="127.0.0.1", port=80, log_level="info")
