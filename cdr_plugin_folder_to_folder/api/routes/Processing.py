from fastapi import APIRouter
from cdr_plugin_folder_to_folder.processing.Loops import Loops

router_params = { "prefix": "/processing"  ,
                  "tags"  : ['Processing'] }

router = APIRouter(**router_params)

@router.post("/start")
def process_hd2_data_to_hd3():
    loops = Loops()
    loops.LoopHashDirectories()
    return "Loop completed"