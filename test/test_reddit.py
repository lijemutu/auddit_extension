# Python code to demonstrate working of unittest 
import unittest 
from src.tasks.scrape_reddit.task import get_hottest_post
from src.tasks.generate_video.task import generate_video
from src.tasks.text_to_speech.task import tts
import json
  
class TestReddit(unittest.TestCase): 
      
    def setUp(self): 
        pass
  
    def test_normal(self): 
        pageName ='eli5'
        with open('doc/'+pageName+'.json') as page:
            page = json.load(page)
            ctx = {
                "subreddit": "askreddit",
                "nsfw": False,
                "comment_limit": 4,
                "page": page
            }
            get_hottest_post(ctx)
            #print(ctx["post"].title)

    def test_video(self):
        pageName ='eli5'
        with open('doc/'+pageName+'.json') as page:
            page = json.load(page)
            ctx = {
                "subreddit": "askreddit",
                "nsfw": False,
                "comment_limit": 4,
                "page": page
            }
            get_hottest_post(ctx)
            tts(ctx)
            generate_video(ctx)



  
if __name__ == '__main__': 
    unittest.main() 
