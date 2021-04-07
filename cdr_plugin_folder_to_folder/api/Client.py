from osbot_utils.utils.Http import GET, GET_json


class Client:

    def __init__(self, url_server):
        self.server_ip = url_server

    def resolve_url(self, path):
        if path.startswith('/'):
            path = path[1:]
        return f"{self.server_ip}/{path}"

    def request_get(self, path):
        url = self.resolve_url(path)
        return GET_json(url)

    def health(self):
        return self.request_get('/health')

    def version(self):
        return self.request_get('/version')


    def file_distributor_hd1(self, num_of_files):
        path = f"/file-distributor/hd1/{num_of_files}"
        return self.request_get(path)