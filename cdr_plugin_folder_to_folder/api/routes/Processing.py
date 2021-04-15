from fastapi import APIRouter
from cdr_plugin_folder_to_folder.processing.Loops import Loops
from cdr_plugin_folder_to_folder.pre_processing.Status import Status
from osbot_utils.utils.Json import json_format

router_params = { "prefix": "/processing"  ,
                  "tags"  : ['Processing'] }

router = APIRouter(**router_params)

@router.post("/start")
def process_hd2_data_to_hd3():
    loops = Loops()
    loops.LoopHashDirectories()
    if loops.HasBeenStopped():
        return "Loop stopped"
    return "Loop completed"

@router.post("/start-sequential")
def process_hd2_data_to_hd3_sequential():
    loops = Loops()
    loops.LoopHashDirectoriesSequential()
    if loops.HasBeenStopped():
        return "Loop stopped"
    return "Loop completed"

@router.post("/stop")
def stop_processing():
    loops = Loops()
    loops.StopProcessing()
    return "Loop stopped"

@router.post("/single_file")
def process_single_file():
    loops = Loops()
    loops.ProcessSingleFile()
    return "File has been processed"

@router.get("/status")
def get_the_processing_status():
    status = Status()
    status.get_from_file()
    return json_format(status.data)