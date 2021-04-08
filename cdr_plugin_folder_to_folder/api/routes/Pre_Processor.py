from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from fastapi import APIRouter

router_params = { "prefix": "/pre-processor"  ,
                  "tags"  : ['Pre Processor'] }
router = APIRouter(**router_params)

@router.post("/pre-process")
def pre_process_hd1_data_to_hd2():
    pre_processor = Pre_Processor()
    pre_processor.process_files()
    return {"Processing is done"}