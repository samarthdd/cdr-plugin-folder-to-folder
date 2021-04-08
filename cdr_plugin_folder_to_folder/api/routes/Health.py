from cdr_plugin_folder_to_folder.common_settings.Config import API_VERSION
from cdr_plugin_folder_to_folder.pre_processing.Pre_Processor import Pre_Processor
from fastapi import APIRouter

router_params = { "prefix": ""  ,
                  "tags"  : ['Health Checks'] }
router = APIRouter(**router_params)

@router.get("/")
def version():
    return health()

@router.get("/health")
def health():
    return { "status": "ok"}

@router.get("/version")
def version():
    return { "version": API_VERSION}