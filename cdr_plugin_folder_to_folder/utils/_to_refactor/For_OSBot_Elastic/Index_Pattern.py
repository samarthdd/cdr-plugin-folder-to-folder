class Index_Pattern:

    def __init__(self, kibana, pattern_name):
        self.kibana       = kibana
        self.pattern_name = pattern_name
        self.object_type  = 'index-pattern'
        pass

    def create(self, time_field=None):
        if self.exists() is False:
            if time_field:
                payload = {"attributes": {"title": self.pattern_name, "fields": "[]", f"timeFieldName": f"{time_field}"}}
            else:
                payload = {"attributes": {"title": self.pattern_name, "fields": "[]"}}

            return self.kibana.post_request(f'api/saved_objects/{self.object_type}', payload)

    def exists(self):
        return self.info() != {}

    def id(self):
        return self.info().get('id')

    def info(self):
        result = self.kibana.index_patterns(index_by='title')
        return result.get(self.pattern_name, {})


    def delete(self):
        object_id = self.id()
        if object_id:
            path = f'api/saved_objects/{self.object_type}/{object_id}'
            self.kibana.delete_request(path)
            return self.exists() is False
        return False