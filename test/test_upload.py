import unittest,os
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

    def test_uploadVideo(self):
        class Post(dict):
            pass
        
        context = {
            'page':{
                'Nombre':"Next level videos",
                'thumbnail': True,
                'description':['Y a ti te ha pasado eso? \nIngresa mi codigo para que ganes dinero!!\nKwai 848290921'],
                'tags':['Amor','Meme','Chistes','Divertido','Reddit'],
                "playlist":"WOOOOOOOW"
            },
            'video_path':os.getcwd()+"\\"+r"test\test_videos\caption.mp4",
            'thumbnail_path':os.getcwd()+"\\"+r"data\thumbnails\8ccd23f7-7292-41d7-a743-b2c9f2b7fd36.png"
            
        }
        post = Post()
        post.title = "titulo de prueba"
        context['post'] = post
        
        upload_video(context)