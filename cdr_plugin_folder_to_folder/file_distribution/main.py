from cdr_plugin_folder_to_folder.file_distribution.File_Distributor import File_Distributor
from fastapi import APIRouter

router = APIRouter()
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




