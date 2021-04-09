import logging

import uvicorn
from fastapi_offline import FastAPIOffline as FastAPI

#from cdr_plugin_folder_to_folder.api.users import router
from osbot_utils.utils.Misc import to_int

from cdr_plugin_folder_to_folder.api.routes.Processing import router as router_processing
from cdr_plugin_folder_to_folder.api.routes.Pre_Processor import router as router_pre_processing
from cdr_plugin_folder_to_folder.api.routes.File_Distributor import router as router_file_distribution
from cdr_plugin_folder_to_folder.api.routes.Health import router as router_health
from cdr_plugin_folder_to_folder.api.routes.Configure import router as router_configure

class Server:

    def __init__(self, app, port="8880", reload=True):
        self.host       = "0.0.0.0"
        self.log_level  = "info"
        self.port       = to_int(port)                                    # todo: move to globally configurable value (set via Env variables)
        self.app        = app
        self.reload     = reload                                              # automatically reloads server on code changes

    def fix_logging_bug(self):
        # there were duplicated entries on logs
        #    - https://github.com/encode/uvicorn/issues/614
        #    - https://github.com/encode/uvicorn/issues/562
        logging.getLogger().handlers.clear()                                # todo: see side effects of this

    def setup(self):
        self.app.include_router(router_processing       )
        self.app.include_router(router_pre_processing   )
        self.app.include_router(router_file_distribution)
        self.app.include_router(router_health           )
        self.app.include_router(router_configure        )
        self.fix_logging_bug()
        return self

    def start(self):
        uvicorn.run("cdr_plugin_folder_to_folder.api.Server:app", host=self.host, port=self.port, log_level=self.log_level, reload=self.reload)

# todo: refactor this into a separate class which can also be used by the individual sections (i.e. tags)
tags_metadata = [
    {"name": "Processing"      , "description": "Step 2"},
    {"name": "Pre Processor"   , "description": "Step 1"},
    {"name": "File Distributor", "description": "Util methods"},
    {"name": "Configaration"   , "description": "Configaration Env"},
]

# we need to do this here so that when unicorn reload is enabled the "cdr_plugin_folder_to_folder.api.Server:app" has an fully setup instance of the Server object
app     = FastAPI(openapi_tags=tags_metadata)
server  = Server(app)
server.setup()

def run_if_main():
    if __name__ == "__main__":
        server.start()

run_if_main()