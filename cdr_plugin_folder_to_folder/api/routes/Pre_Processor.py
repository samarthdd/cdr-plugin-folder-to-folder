from osbot_utils.utils.Status import status_ok

from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from fastapi import APIRouter

router_params = { "prefix": "/pre-processor"  ,
                  "tags"  : ['Pre Processor'] }
router = APIRouter(**router_params)

@router.post("/pre-process")
def pre_process_hd1_data_to_hd2():
    pre_processor = Pre_Processor()
    pre_processor.process_files()
    return {"Processing is done"}                   # todo: refactor to use status_ok helper methods (as seen in clear_data_and_status_folders )

@router.post("/clear-data-and-status")
def clear_data_and_status_folders():
    pre_processor = Pre_Processor()
    pre_processor.clear_data_and_status_folders()
    return status_ok(message="Data cleared from HD2")