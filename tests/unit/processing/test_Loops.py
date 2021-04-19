import asyncio
from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from cdr_plugin_folder_to_folder.processing.Loops import Loops
from cdr_plugin_folder_to_folder.utils.testing.Setup_Testing import Setup_Testing


class test_Loops(TestCase):

    def setUp(self) -> None:
        Setup_Testing()
        self.loops = Loops()

    def test_LoopHashDirectories(self):
        self.loops.LoopHashDirectories()

    def test_LoopHashDirectoriesAsync(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.loops.LoopHashDirectoriesAsync(thread_count=1))

    def test_LoopHashDirectoriesInternal(self):
        self.loops.LoopHashDirectoriesInternal(thread_count=1, do_single=False)

