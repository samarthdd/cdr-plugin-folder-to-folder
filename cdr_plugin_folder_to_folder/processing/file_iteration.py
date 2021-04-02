import os
import os.path
import sys
sys.path.insert(1, '../common_settings')
from config_params import Config
from file_processing import FileProcessing

class FileOperations(object):

    @staticmethod
    def LoopHashDirectories():
        rootdir = os.path.join(Config.hd2_location,"data")
        directory_contents = os.listdir(rootdir)
        for item in directory_contents:
            itempath = os.path.join(rootdir,item)
            if os.path.isdir(itempath):
                print(itempath)
                FileProcessing.processDirectory(itempath)

    @staticmethod
    def main(argv):
        FileOperations.LoopHashDirectories()

if __name__ == "__main__":
    FileOperations.main(sys.argv[1:])