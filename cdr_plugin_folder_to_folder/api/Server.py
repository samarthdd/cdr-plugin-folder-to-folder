import uvicorn
from fastapi import FastAPI

#from cdr_plugin_folder_to_folder.api.users import router
from cdr_plugin_folder_to_folder.processing.main import router as processing_router
from cdr_plugin_folder_to_folder.pre_processing.main import router as pre_processing_router
from cdr_plugin_folder_to_folder.file_distribution.main import router as file_distribution_router


class Server:

    def __init__(self):
        self.host       = "0.0.0.0"
        self.log_level  = "info"
        self.port       = 8880
        self.app        = None

    def setup(self):
        self.app = FastAPI()
        self.app.include_router(processing_router, prefix="")
        self.app.include_router(pre_processing_router, prefix="")
        self.app.include_router(file_distribution_router, prefix="/get_files")
        return self

    def start(self):
        uvicorn.run(self.app, host=self.host, port=int(self.port), log_level=self.log_level)

if __name__ == "__main__":
    Server().setup().start()