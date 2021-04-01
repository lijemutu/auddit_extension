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
                'description':['Y a ti te ha pasado eso?','Cuentanos tu experiencia y dejanos un like', 'Sigue nuestra página para ver más contenido así :D'],
                'tags':['Amor','Meme','Chistes','Divertido','Reddit']
            },
            'video_path':os.getcwd()+"\\"+r"data\video\1c995722-3eef-47a5-bf0b-2c94e4dc2354.mp4",
            'thumbnail_path':os.getcwd()+"\\"+r"data\thumbnails\4e4ff322-f55c-4d96-a727-6eb95693a537.png"
            
        }
        post = Post()
        post.title = "titulo de prueba"
        context['post'] = post
        print(context['post'].title)
        upload_video(context)