import os
import os.path
import sys

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from file_processing import FileProcessing

class Loops(object):

    @staticmethod
    def LoopHashDirectories():
        config = Config().load_values()
        rootdir = os.path.join(config.hd2_location,"data")
        directory_contents = os.listdir(rootdir)
        for item in directory_contents:
            itempath = os.path.join(rootdir,item)
            if os.path.isdir(itempath):
                print("Processing: ", itempath)
                FileProcessing.processDirectory(itempath)

    @staticmethod
    def main(argv):
        Loops.LoopHashDirectories()

if __name__ == "__main__":
    Loops.main(sys.argv[1:])
