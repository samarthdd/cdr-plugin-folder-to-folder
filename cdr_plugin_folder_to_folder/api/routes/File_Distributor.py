from cdr_plugin_folder_to_folder.file_distribution.File_Distributor import File_Distributor
from fastapi import APIRouter

router_params = { "prefix": "/file-distributor"  ,
                  "tags"  : ['File Distributor'] }
router        = APIRouter(**router_params)
file_distributor = File_Distributor()

@router.get("/hd1/{num_of_files}")
def get_hd1_files(num_of_files: int):
    list=file_distributor.get_hd1_files(num_of_files=num_of_files)
    return list

@router.get("/hd2/metadata/{num_of_files}")
def get_hd2_metadata_files(num_of_files: int):
    list=file_distributor.get_hd2_metadata_files(num_of_files=num_of_files)
    return list

@router.get("/hd2/source/{num_of_files}")
def get_hd2_source_files(num_of_files: int):
    list=file_distributor.get_hd2_source_files(num_of_files=num_of_files)
    return list

@router.get("/hd2/report/{num_of_files}")
def get_hd2_report_files(num_of_files: int):
    list=file_distributor.get_hd2_report_files(num_of_files=num_of_files)
    return list

@router.get("/hd2/hash_folder_list/{num_of_files}")
def get_hd2_hash_folders_files(num_of_files : int):
    list=file_distributor.get_hd2_hash_folder_list(num_of_files=num_of_files)
    return list

@router.get("/hd2/status")
def get_hd2_status_files():
    list=file_distributor.get_hd2_status_hash_file()
    return list

@router.get("/hd3/{num_of_files}")
def get_hd3_files(num_of_files: int):
    list=file_distributor.get_hd3_files(num_of_files=num_of_files)
    return list

@router.get("/configure_hard_discs}")
def get_hd3_files(hd1_path: str=None,hd2_path: str=None,hd3_path: str=None):
    list=file_distributor.configure_hard_discs(hd1_path=hd1_path,hd2_path=hd2_path,hd3_path=hd3_path)
    return list