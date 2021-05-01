from cdr_plugin_folder_to_folder.file_distribution.File_Distributor import File_Distributor
from fastapi import APIRouter, Query
from typing import  Optional
import ntpath
router_params = { "prefix": "/file-distributor"  ,
                  "tags"  : ['File Distributor'] }
router        = APIRouter(**router_params)

from starlette.responses import FileResponse

@router.get("/hd2/status")
def get_hd2_status_files():
    file_distributor = File_Distributor()
    file_response    = file_distributor.get_hd2_status()

    if file_response == -1 :
        return "hd2/status folder is empty"
    return FileResponse(file_response, media_type='application/octet-stream', filename=ntpath.basename(file_response))

@router.get("/hd2/data")
def get_hd2_processed_files(num_of_files: int = Query(-1, description="Keep -1 to get all hd2/data",)):
    if num_of_files == 0 :
        return "Invalid value for num_of_files"
    file_distributor = File_Distributor()
    file_response    = file_distributor.get_hd2_data(num_of_files=num_of_files)

    if file_response == -1 :
        return "hd2/data folder is empty"

    return FileResponse(file_response, media_type='application/octet-stream', filename=ntpath.basename(file_response))

@router.get("/hd2/processed")
def get_hd2_processed_files(num_of_files: int = Query(-1, description="Keep -1 to get all hd2/processed data",)):
    if num_of_files == 0 :
        return "Invalid value for num_of_files"

    file_distributor = File_Distributor()
    file_response    = file_distributor.get_hd2_processed(num_of_files=num_of_files)

    if file_response == -1 :
        return "hd2/processed folder is empty"

    return FileResponse(file_response, media_type='application/octet-stream', filename=ntpath.basename(file_response))

# @router.get("/hd3/{num_of_files}")
# def get_hd3_files(num_of_files: int):
#     file_distributor = File_Distributor()
#     file_path=file_distributor.get_hd3_files(num_of_files=num_of_files)
#     return FileResponse(file_path, media_type='application/octet-stream', filename=ntpath.basename(file_path))
