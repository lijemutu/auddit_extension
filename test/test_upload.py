import unittest
from src.tasks.upload_video.task import upload_video
class TestReddit(unittest.TestCase):

    def setUp(self):
        pass

    def test_upload(self):
        context = {
            'page':{
                'Nombre':'Next level videos'
            }
        }
        upload_video(context)