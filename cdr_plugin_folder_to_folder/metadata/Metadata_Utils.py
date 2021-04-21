from osbot_utils.utils.Files import file_sha256, file_exists


class Metadata_Utils:

    def file_hash(self, file_path):
        if file_exists(file_path):
            return file_sha256(file_path)