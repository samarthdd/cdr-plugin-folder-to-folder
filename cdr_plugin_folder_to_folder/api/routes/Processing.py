from fastapi import APIRouter
from cdr_plugin_folder_to_folder.processing.Loops import Loops

router_params = { "prefix": "/processing"  ,
                  "tags"  : ['Processing'] }

router = APIRouter(**router_params)

@router.get("/")
def read_root():
    return "FastAPI Home"

@router.get("/loop")
def run_the_loop():
    Loops.LoopHashDirectories()
    return "Loop completed"