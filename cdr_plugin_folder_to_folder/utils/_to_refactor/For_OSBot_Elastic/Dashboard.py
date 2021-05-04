from osbot_utils.utils.Files import file_create
from osbot_utils.utils.Http import GET


class Dashboard:

    def __init__(self, kibana, dashboard_name=None, dashboard_id=None):
        self.kibana         = kibana
        self.dashboard_name = dashboard_name
        self.dashboard_id   = dashboard_id
        self.object_type    = 'dashboard'
        pass

    def create(self):
        if self.exists() is False:
            payload = {}
            # if time_field:
            #     payload = {"attributes": {"title": self.pattern_name, "fields": "[]", f"timeFieldName": f"{time_field}"}}
            # else:
            #     payload = {"attributes": {"title": self.pattern_name, "fields": "[]"}}

            return self.kibana.post_request(f'api/saved_objects/{self.object_type}', payload)

    def exists(self):
        return self.info() != {}

    def id(self):
        return self.info().get('id')

    def info(self):
        result = self.kibana.index_patterns(index_by='title')
        return result.get(self.dashboard_name, {})


    def delete(self):
        object_id = self.id()
        if object_id:
            path = f'api/saved_objects/{self.object_type}/{object_id}'
            self.kibana.delete_request(path)
            return self.exists() is False
        return False

    def export_dashboard(self):
        path = "api/saved_objects/_export"
        payload = {"objects":[{"id":self.dashboard_id,"type":"dashboard"}],"includeReferencesDeep":True}

        export_data = self.kibana.post_request(path=path, payload=payload, parse_into_json=False)
        return export_data

    def import_dashboard(self, import_file):
        path = "api/saved_objects/_import?overwrite=true"
        #payload = {"objects":[{"id":self.dashboard_id,"type":"dashboard"}],"includeReferencesDeep":True}

        return self.kibana.post_file(path=path,path_file=import_file, parse_into_json=False)

    def import_dashboard_from_github(self, dashboard_file_name):
        url_dashboards = 'https://raw.githubusercontent.com/filetrust/cdr-plugin-folder-to-folder-test-data/main/kibana-dashboards/'
        url_dashboard = url_dashboards + dashboard_file_name
        dashboard_data = GET(url_dashboard)

        import_file = file_create(extension=dashboard_file_name, contents=dashboard_data)
        return self.import_dashboard(import_file= import_file)
