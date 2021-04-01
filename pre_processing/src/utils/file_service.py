import os
import shutil

class FileService:
    def copy_file(self,src,dst):
        try:
            shutil.copyfile(src, dst)
        except Exception as error:
            raise error

    def copy_folder(self,src,dest):
        try:
            shutil.copytree(src, dest)
        except Exception as error:
            raise error

    def move_file(self,src,dst):
        try:
            shutil.move(src, dst)
        except Exception as error:
            raise error

    def wrtie_file(self,folder,file_name,content):
        try:
            self.metadata_file_name = os.path.join(folder, file_name)
            with open(self.metadata_file_name, "w") as fp:
                fp.write(str(content))
        except Exception as error:
            raise error

    def create_folder(self,folder_name):
        try:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
        except Exception as error:
            raise error

    def delete_folder(self,folder_path):
        try:
            shutil.rmtree(folder_path)
        except Exception as error:
            raise error

