from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from fastapi import APIRouter

router = APIRouter()
pre_processor = Pre_Processor()

@router.get("/pre-process")
def start_pre_process():
    pre_processor.process_files()
    return {"Processing is done"}