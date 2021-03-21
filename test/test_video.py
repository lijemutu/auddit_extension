# Python code to demonstrate working of unittest
import unittest
from src.tasks.scrape_reddit.task import get_hottest_post
from src.tasks.generate_video.task import generate_video
from src.tasks.generate_video.task import generate_title
from src.tasks.text_to_speech.task import save_tts, save_gtts, save_ttsService
import json


class TestVideo(unittest.TestCase):

    def setUp(self):
        pass


    def test_video_Video(self):
        pageName = 'redditVideos'
        with open('doc/'+pageName+'.json') as page:
            page = json.load(page)
            ctx = {
                "nsfw": False,
                "comment_limit": 4,
                "page": page
            }
            test_videos = [
                    {
                        'title':'Video de prueba',
                        'author':'test',
                        'permalink':'test',
                        'video_path':'C:\\Users\\erick\\projects\\auddit\\test\\test_videos\\seconds20height720width576.mp4',
                        'score':1,
                        'width':576,
                        'height':720
                    }
                ]
            
            ctx['post'] = test_videos
            generate_video(ctx)


    def test_Video_title(self):
        path = "C:\\Users\\erick\\projects\\auddit\\test\\test_videos\\title.mp4"
        text = save_tts("¿Cual ha sido tu historia más chistosa?")
        pageName = 'preguntas_reddit_mex'
        with open('doc/'+pageName+'.json') as page:
            page = json.load(page)
            ctx = {
                "nsfw": False,
                "comment_limit": 4,
                "page": page
            }
            clip =generate_title(text="¿Cual ha sido tu historia más chistosa ?",audio_path=text,page=ctx['page'])
            clip.write_videofile(path, fps=24, codec='libx264', threads=4)

