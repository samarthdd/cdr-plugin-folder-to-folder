import os
import os.path
import sys
sys.path.insert(1, '../common_settings')
from config_params import Config
from file_processing import FileProcessing

from fastapi import FastAPI
from starlette import status
from starlette.responses import Response

class Loops(object):

    @staticmethod
    def LoopHashDirectories():
        rootdir = os.path.join(Config.hd2_location,"data")
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
