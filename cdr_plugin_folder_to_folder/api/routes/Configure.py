import json

from cdr_plugin_folder_to_folder.common_settings.Config import API_VERSION, Config
from cdr_plugin_folder_to_folder.configure.Configure_Env import Configure_Env
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, HTTPException

configure_env=Configure_Env()
router_params = { "prefix": "/configuration"  ,
                  "tags"  : ['Configuration'] }

class CONFIGURATION(BaseModel):
    hd1_path   : str = "./test_data/scenario-1/hd1"
    hd2_path   : str = "./test_data/scenario-1/hd2"
    hd3_path   : str = "./test_data/scenario-1/hd3"

class ENDPOINTS(BaseModel):
    IP         : str
    Port       : str

class ItemList(BaseModel):
    Endpoints : List[ENDPOINTS]

router = APIRouter(**router_params)

@router.get("/config/")
def config():
    return Config().values()

@router.post("/configure_env/",response_model=CONFIGURATION)
def configure_environment(item: CONFIGURATION):
    response = configure_env.configure(hd1_path=item.hd1_path,
                                       hd2_path=item.hd2_path,
                                       hd3_path=item.hd3_path)

    if response == -1 :
        raise HTTPException(status_code=404, detail="Data Paths are not valid")

    return response


@router.post("/configure_gw_sdk_endpoints/")
def configure_multiple_gw_sdk_endpoints(item: ItemList):
    json_item=item.json()
    response = configure_env.configure_endpoints(endpoint_string=json_item)
    if response == -1 :
        raise HTTPException(status_code=404, detail="GW_sdk_endpoints are not valid")
    return response

