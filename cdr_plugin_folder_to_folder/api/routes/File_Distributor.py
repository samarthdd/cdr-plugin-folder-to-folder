from cdr_plugin_folder_to_folder.file_distribution.File_Distributor import File_Distributor
from fastapi import APIRouter, Query
from typing import  Optional
import ntpath
router_params = { "prefix": "/file-distributor"  ,
                  "tags"  : ['File Distributor'] }
router        = APIRouter(**router_params)

from starlette.responses import FileResponse

# @router.get("/hd1/{num_of_files}")
# def get_hd1_files(num_of_files: int):
#     file_distributor = File_Distributor()
#     file_path=file_distributor.get_hd1_files(num_of_files=num_of_files)
#     return FileResponse(file_path, media_type='application/octet-stream', filename=ntpath.basename(file_path))

# @router.get("/hd2/metadata/{num_of_files}")
# def get_hd2_metadata_files(num_of_files: int):
#     file_distributor = File_Distributor()
#     file_path=file_distributor.get_hd2_metadata_files(num_of_files=num_of_files)
#     return FileResponse(file_path, media_type='application/octet-stream', filename=ntpath.basename(file_path))

# @router.get("/hd2/source/{num_of_files}")
# def get_hd2_source_files(num_of_files: int):
#     file_distributor = File_Distributor()
#     file_path=file_distributor.get_hd2_source_files(num_of_files=num_of_files)
#     return FileResponse(file_path, media_type='application/octet-stream', filename=ntpath.basename(file_path))

# @router.get("/hd2/report/{num_of_files}")
# def get_hd2_report_files(num_of_files: int):
#     file_distributor = File_Distributor()
#     file_path=file_distributor.get_hd2_report_files(num_of_files=num_of_files)
#     return FileResponse(file_path, media_type='application/octet-stream', filename=ntpath.basename(file_path))

# @router.get("/hd2/hash_folder_list/{num_of_files}")
# def get_hd2_hash_folders_files(num_of_files : int):
#     file_distributor = File_Distributor()
#     file_path=file_distributor.get_hd2_hash_folder_list(num_of_files=num_of_files)
#     return FileResponse(file_path, media_type='application/octet-stream', filename=ntpath.basename(file_path))

@router.get("/hd2/status")
def get_hd2_status_files():
    file_distributor = File_Distributor()
    file_path=file_distributor.get_hd2_status_hash_file()
    return FileResponse(file_path, media_type='application/octet-stream', filename=ntpath.basename(file_path))

@router.get("/hd2/processed")
def get_hd2_processed_files(num_of_files: int = Query(-1, description="Keep -1 to get all hd2/processed data",)):
    if num_of_files == 0 :
        return "Invalid value for num_of_files"
    file_distributor = File_Distributor()
    file_path=file_distributor.get_hd2_processed(num_of_files=num_of_files)
    return FileResponse(file_path, media_type='application/octet-stream', filename=ntpath.basename(file_path))

# @router.get("/hd3/{num_of_files}")
# def get_hd3_files(num_of_files: int):
#     file_distributor = File_Distributor()
#     file_path=file_distributor.get_hd3_files(num_of_files=num_of_files)
#     return FileResponse(file_path, media_type='application/octet-stream', filename=ntpath.basename(file_path))
