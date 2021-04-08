from fastapi                                import FastAPI
from starlette.testclient                   import TestClient
from cdr_plugin_folder_to_folder.api.Server import Server

class Direct_API_Server:

    def __init__(self):
        self.app    = None
        self.server = None
        self.client = None

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def setup(self):
        self.app    = FastAPI()
        self.server = Server(self.app).setup()
        self.client = TestClient(self.app)
        return self

    def GET(self, path='/', headers=None):
        return self.client.get(path, headers=headers).json()

    def POST(self, path='/', headers=None,json=None):
        return self.client.post(path, headers=headers,json=json).json()