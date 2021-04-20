from multiprocessing.context import Process
from urllib.parse import urljoin

from fastapi_offline import FastAPIOffline as FastAPI
from osbot_utils.utils.Http import GET_json
from osbot_utils.utils.Misc import random_port, wait_for

from cdr_plugin_folder_to_folder.api.Server import Server


def run_server(port):
    app = FastAPI()
    Server(app=app, port=port, reload=False).add_routes().start()


class Temp_API_Server:

    def __init__(self):
        self.port = random_port()
        self.proc = None

    def __enter__(self):
        self.start_server()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_server()

    def http_GET(self, path=''):
        try:
            full_url = urljoin(self.server_url(), path)
            return GET_json(full_url)
        except:
            return None

    def server_running(self):
        return self.proc.is_alive()

    def start_server(self):
        self.proc = Process(target=run_server, args=[self.port])
        self.proc.start()
        return self.wait_for_server_ok()

    def stop_server(self):
        self.proc.kill()
        self.proc.join()

    def server_url(self):
        return f"http://127.0.0.1:{self.port}"

    def wait_for_server_ok(self, max_attempts=20, wait_interval=0.1):
        for i in range(0,max_attempts):
            status = self.http_GET('/health')
            if status:
                return status
            wait_for(wait_interval)