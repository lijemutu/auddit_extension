# Python code to demonstrate working of unittest
import unittest
from src.tasks.scrape_reddit.task import get_hottest_post,translateEditComments
from src.tasks.generate_video.task import generate_video
from src.tasks.text_to_speech.task import tts
import json
from unittest.mock import patch
from io import StringIO


class TestReddit(unittest.TestCase):

    def setUp(self):
        pass

    def test_normal(self):
        pageName = 'redditVideos'
        with open('doc/'+pageName+'.json') as page:
            page = json.load(page)
            ctx = {
                "nsfw": False,
                "comment_limit": 4,
                "page": page
            }
            get_hottest_post(ctx)
            # print(ctx["post"].title)

    def test_video_Text(self):
        pageName = 'preguntas_reddit_mex'
        with open('doc/'+pageName+'.json') as page:
            page = json.load(page)
            ctx = {
                "nsfw": False,
                "comment_limit": 4,
                "page": page
            }
            print("task: get_hottest_post")
            get_hottest_post(ctx)
            print("task: generate video")
            generate_video(ctx)

    def test_video_Video(self):
        pageName = 'redditVideos'
        with open('doc/'+pageName+'.json') as page:
            page = json.load(page)
            ctx = {
                "nsfw": False,
                "comment_limit": 4,
                "page": page
            }
            print("task: get_hottest_post")
            get_hottest_post(ctx)
            print("task: generate video")
            generate_video(ctx)

    @patch("sys.stdin", StringIO("titulo corregido\ncomentario corregido1\n^Z\n comentario corregido 2\n^Z\n"))
    def test_editComments(self):
        class Post(dict):
            pass
        post = Post()
        post.title ='Titulo de prueba'
        post.comments = [Post(),Post()]
        post.comments[0].body = 'Pruebba0'
        post.comments[1].body = 'Pruebba1'
        translateEditComments(post)



if __name__ == '__main__':
    unittest.main()
