# Python code to demonstrate working of unittest
import unittest
from src.tasks.cleanup.task import cleanup


class TestClean(unittest.TestCase):

    def setUp(self):
        pass


    def test_clean(self):
        context = {}
        cleanup(context)
